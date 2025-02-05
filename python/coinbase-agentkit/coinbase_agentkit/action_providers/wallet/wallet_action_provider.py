from decimal import Decimal
from typing import Dict, Any
from pydantic import BaseModel

from ..action_provider import ActionProvider
from ..action_decorator import CreateAction
from ...wallet_providers import WalletProvider
from ...network import Network

class GetWalletDetailsSchema(BaseModel):
    """Input schema for getting wallet details."""
    pass

class WalletActionProvider(ActionProvider[WalletProvider]):
    """Provides actions for interacting with wallet functionality."""
    
    def __init__(self):
        super().__init__("wallet", [])

    @CreateAction(
        name="get_wallet_details",
        description="""
    This tool will return the details of the connected wallet including:
    - Wallet address
    - Network information (protocol family, network ID, chain ID)
    - ETH token balance
    - Native token balance
    - Wallet provider name
    """,
        schema=GetWalletDetailsSchema
    )
    def get_wallet_details(
        self,
        args: Dict[str, Any]
    ) -> str:
        """Get details about the wallet."""
        try:
            wallet_address = self.wallet_provider.get_address()
            network = self.wallet_provider.get_network()
            balance = self.wallet_provider.get_balance()
            provider_name = self.wallet_provider.get_name()
            
            # Convert balance from Wei to ETH
            eth_balance = Decimal(str(balance)) / Decimal('1000000000000000000')
            
            return f"""Wallet Details:
- Provider: {provider_name}
- Address: {wallet_address}
- Network: 
  * Protocol Family: {network.protocol_family}
  * Network ID: {network.network_id or "N/A"}
  * Chain ID: {str(network.chain_id) if network.chain_id else "N/A"}
- ETH Balance: {eth_balance:.6f} ETH
- Native Balance: {balance} WEI"""
        except Exception as e:
            return f"Error getting wallet details: {e}"

    def supports_network(self, network: Network) -> bool:
        """Check if network is supported by wallet actions."""
        return True

def wallet_action_provider() -> WalletActionProvider:
    """Create a new WalletActionProvider instance."""
    return WalletActionProvider()
