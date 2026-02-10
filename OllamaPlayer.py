from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage
from dotenv import load_dotenv
import os

load_dotenv()


class OllamaPlayer:
    def __init__(self, player_name):
        # set name
        self.name = player_name
        
        # load environment variables
        server_ip = os.getenv("LLM_SERVER_IP", "127.0.0.1")
        server_port = os.getenv("LLM_PORT","11434")
        model_name = os.getenv("LLM_MODEL","llama3.1:8b")
        
        # initialize llm and bind tools
        self.llm = ChatOllama(base_url=f"http://{server_ip}:{server_port}",
                              model=model_name)

        self.messages = [
            SystemMessage("""GAME: Coup

        OBJECTIVE:
        Be the last remaining player with at least one influence.
        
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
        """)]
                          
                          
                          
    def set_cards(self,card1, card2):
        self.card1 = card1
        self.card2 = card2
                       
        
        
    def update(self):
        pass
    
    
    def take_turn(self, n_coins, card1, card2):
        self.messages.append(HumanMessage("It is your turn. you have {n_coins} coins, {card1} and {card2}. what would you like to do?"))
        response = self.llm.invoke(self.messages)
        return response.content
    
    
    