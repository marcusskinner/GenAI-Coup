from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage
from dotenv import load_dotenv
import json
import os


from TurnAction import TurnAction
from ResponseAction import ResponseAction

load_dotenv()


class OllamaPlayer:
    def __init__(self, player_name, personality="None"):
        # set name
        self.name = player_name
        
        # load environment variables
        server_ip = os.getenv("LLM_SERVER_IP", "127.0.0.1")
        server_port = os.getenv("LLM_PORT","11434")
        model_name = os.getenv("LLM_MODEL","llama3.1:8b")
        
        # initialize llm and bind tools
        self.llm = ChatOllama(base_url=f"http://{server_ip}:{server_port}",
                              model=model_name)
        self.personality = SystemMessage(personality)
        self.rules = SystemMessage("""
        GAME: Coup

        OBJECTIVE:
        Be the last remaining player with at least one influence.
        
        If you attempt to do something on your turn that you are not able to do, 
        you will lose an influence card. 
        
        INFLUENCE:
        Each player starts with 2 hidden influence cards.
        If a player loses all influence, they are eliminated.
        
        COINS:
        Each player starts with 2 coins.
        Coins are public information.
        
        ACTIONS:
        On your turn, you must take exactly one action.
        
        Income:
        - Gain 1 coin.
        - Cannot be blocked or challenged.
        
        Foreign Aid:
        - Gain 2 coins.
        - Can be blocked by Duke.
        
        Coup:
        - Cost: 7 coins (mandatory if you have 10 or more).
        - Choose a target player.
        - Target loses 1 influence.
        - Cannot be blocked or challenged.
        
        CHARACTER ACTIONS (require claiming the role):
        Duke:
        - Take 3 coins (Tax).
        - Block Foreign Aid.
        
        Assassin:
        - Pay 3 coins.
        - Target player loses 1 influence.
        - Can be blocked by Contessa.
        
        Captain:
        - Steal 2 coins from another player.
        - Can be blocked by Captain or Ambassador.
        
        Ambassador:
        - Exchange cards with the deck.
        - Can block Captain.
        
        Contessa:
        - Blocks assassination.
        
        CHALLENGES:
        Any player may challenge a claimed role action or block.
        - If the challenger is wrong, they lose 1 influence.
        - If the challenged player is lying, they lose 1 influence and the action is canceled.
        
        BLOCKS:
        Blocks must claim a valid blocking role.
        Blocks may be challenged.
        
        LYING:
        Players may claim any role, even if they do not have it.      
        
        ADDITIONAL RULES:
        - The deck contains exactly 3 copies of each role.
        - When a player loses influence, the chosen card is revealed face up and remains visible for the rest of the game.
        - Revealed cards are not returned to the deck.
        - All revealed cards are public information.
        
        """)
                          
    
    def take_turn(self, player_info, table_info):
        message = [self.personality, self.rules, HumanMessage(f"It is your turn. Your hand: {player_info}, game state: {table_info}. Respond with only a json containing the action_name (all lowercase) and the target_player if the card you are playing is targeting an opponent, otherwise target_player should be None. The name of the Action options are: 'income', 'foreign aid', 'coup', 'tax', 'steal', 'exchange'.")]
        response = self.llm.invoke(message)
        try:
            json_action = json.loads(response.content)
            a_name = json_action['action_name']
            a_name = a_name.lower()
            target_player = json_action.get('target_player', None)
            if a_name in ['income', 'foreign aid','coup', 'tax','assassinate','steal', 'exchange' ]:
                action = TurnAction(self.name, a_name, target_player)
            elif 'ambassador' in a_name or 'exchange' in a_name:
                action = TurnAction(self.name, 'exchange', target_player)
            elif 'assassin' in a_name:
                action = TurnAction(self.name, 'assassinate',target_player)
            elif 'captain' in a_name or 'steal' in a_name:
                action = TurnAction(self.name, 'steal', target_player)
            elif 'foreign' in a_name:
                action = TurnAction(self.name, 'foreign aid', target_player)
            elif 'duke' in a_name or 'tax' in a_name:
                action = TurnAction(self.name, 'tax', target_player)
            else:
                action = TurnAction(self.name, 'error',target_player)
                
            #print("Attempt: ", action.summary)
            return action
        except:
            print("Error 1a, Response: ", response.content)

    
    def lose_card(self, player_info, table_info):
        message = [self.rules, HumanMessage(f"You are losing a influence card. You may select which card to give up. Your hand: {player_info}, game state:{table_info}. Respond with only the name of the card to give up.")]
        response = self.llm.invoke(message)
        #print(self.name, "Lost Card :", response.content)
        return response.content
            
    
    def exchange(self, player_info, table_info, cards_drawn):
        message = [self.rules, HumanMessage(f"You are using an Ambassador to exchange cards. Your hand: {player_info}, game state: {table_info}. The cards you have drawn: {cards_drawn}. Choose which cards to keep and which to discard in accordance with the rules. Return only a JSON containing keep: python list of cards to keep. The number of cards you keep must be the same as the number currently facedown.")]
        response = self.llm.invoke(message)
        try:
            json_exchange = json.loads(response.content)
            keep = json_exchange['keep']
            return keep
        except:
            print("Error 2", response.content)
            return player_info['facedown']
            
    
    def respond(self, player_info, table_info, action):
        message = [self.rules, HumanMessage(f"An opponent is taking their turn and you need to decide if you want to block or challenge. If you do not want to block or challenge you may pass. Your hand: {player_info}, game state: {table_info}, Action Information - {action.summary}. Respond as a json with the 'action: 'block', 'challenge', or 'pass' and if you are blocking use 'claimed_card' : card name (capitalized).")]
        response = self.llm.invoke(message)
       
        # default response if LLM fails
        resp = ResponseAction(self.name, "pass", None)

        try:
            json_resp = json.loads(response.content)
            action_name = json_resp['action']
            claimed_card = json_resp.get('claimed_card')
            resp = ResponseAction(self.name, action_name, claimed_card)
            # print("Responded: ", resp.summary)
        except:
            print("Error 3", response.content)
            
        return resp
        
        