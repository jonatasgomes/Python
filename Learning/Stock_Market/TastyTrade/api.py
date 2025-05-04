"""
TastyTrade API Python Example
------------------------------
This script demonstrates how to interact with the TastyTrade API using Python requests.
Features demonstrated:
- Authentication
- Account information retrieval
- Market data retrieval
- Placing and monitoring orders (simulated)
"""
import requests
from typing import Dict, List, Any, Optional
import env

class TastyTradeAPI:
    """Class to interact with the TastyTrade API"""
    
    # API endpoints
    BASE_URL_CERT = "https://api.cert.tastyworks.com"  # Certification environment
    BASE_URL_PROD = "https://api.tastyworks.com"       # Production environment
    
    def __init__(self, username: str, password: str, use_prod: bool = False):
        """Initialize the TastyTrade API client
        
        Args:
            username: TastyTrade account username
            password: TastyTrade account password
            use_prod: If True, use production environment, otherwise use certification
        """
        self.username = username
        self.password = password
        self.base_url = self.BASE_URL_PROD if use_prod else self.BASE_URL_CERT
        self.session_token = None
        self.accounts = []
        
    def authenticate(self) -> bool:
        """Authenticate with TastyTrade API
        
        Returns:
            bool: True if authentication was successful
        """
        url = f"{self.base_url}/sessions"
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "login": self.username,
            "password": self.password
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            data = response.json()
            self.session_token = data["data"]["session-token"]
            
            # Update headers with session token for future requests
            self._update_auth_headers()
            
            print("Authentication successful!")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"Authentication failed: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return False
    
    def _update_auth_headers(self) -> Dict[str, str]:
        """Update headers with authentication token
        
        Returns:
            Dict containing headers with authentication token
        """
        return {
            "Authorization": f"{self.session_token}",
            "Content-Type": "application/json"
        }
    
    def get_accounts(self) -> List[Dict[str, Any]]:
        """Get all accounts associated with the authenticated user
        
        Returns:
            List of account dictionaries
        """
        if not self.session_token:
            print("Not authenticated. Please authenticate first.")
            return []
        
        url = f"{self.base_url}/customers/me/accounts"
        headers = self._update_auth_headers()
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            self.accounts = data["data"]["items"]
            
            print(f"Retrieved {len(self.accounts)} accounts")
            return self.accounts
            
        except requests.exceptions.RequestException as e:
            print(f"Failed to get accounts: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return []
    
    def get_account_balances(self, account_number: str) -> Dict[str, Any]:
        """Get balance information for a specific account
        
        Args:
            account_number: The account number to query
            
        Returns:
            Dict containing account balance information
        """
        if not self.session_token:
            print("Not authenticated. Please authenticate first.")
            return {}
        
        url = f"{self.base_url}/accounts/{account_number}/balances"
        headers = self._update_auth_headers()
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            return data["data"]
            
        except requests.exceptions.RequestException as e:
            print(f"Failed to get account balances: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return {}
    
    def get_quote(self, symbols: List[str]) -> Dict[str, Any]:
        """Get market quotes for specified symbols
        
        Args:
            symbols: List of symbols to get quotes for
            
        Returns:
            Dict containing quote information
        """
        if not self.session_token:
            print("Not authenticated. Please authenticate first.")
            return {}
        
        # Join symbols with commas for the query parameter
        symbols_str = ",".join(symbols)
        
        url = f"{self.base_url}/quotes"
        headers = self._update_auth_headers()
        params = {
            "symbols": symbols_str
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            return data["data"]["items"]
            
        except requests.exceptions.RequestException as e:
            print(f"Failed to get quotes: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return {}
    
    def get_option_chains(self, symbol: str) -> Dict[str, Any]:
        """Get option chain data for a symbol
        
        Args:
            symbol: The underlying symbol
            
        Returns:
            Dict containing option chain data
        """
        if not self.session_token:
            print("Not authenticated. Please authenticate first.")
            return {}
        
        url = f"{self.base_url}/option-chains/{symbol}"
        headers = self._update_auth_headers()
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            return data["data"]["items"]
            
        except requests.exceptions.RequestException as e:
            print(f"Failed to get option chains: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return {}
    
    def place_equity_order(self, account_number: str, symbol: str, quantity: int, 
                           order_type: str = "Limit", price: Optional[float] = None,
                           side: str = "Buy", time_in_force: str = "Day") -> Dict[str, Any]:
        """Place an equity order
        
        Args:
            account_number: Account number to place the order for
            symbol: Stock symbol
            quantity: Number of shares
            order_type: Type of order (Market, Limit, etc.)
            price: Price for limit orders
            side: Buy or Sell
            time_in_force: Day, GTC, etc.
            
        Returns:
            Dict containing order response
        """
        if not self.session_token:
            print("Not authenticated. Please authenticate first.")
            return {}
        
        url = f"{self.base_url}/accounts/{account_number}/orders"
        headers = self._update_auth_headers()
        
        # Build order payload
        payload = {
            "order": {
                "type": order_type,
                "time-in-force": time_in_force,
                "price": price,
                "price-effect": "Debit",
                "legs": [
                    {
                        "instrument-type": "Equity",
                        "symbol": symbol,
                        "quantity": quantity,
                        "action": side
                    }
                ]
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            data = response.json()
            print(f"Order placed successfully")
            return data["data"]
            
        except requests.exceptions.RequestException as e:
            print(f"Failed to place order: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return {}
    
    def get_positions(self, account_number: str) -> List[Dict[str, Any]]:
        """Get current positions for a specific account
        
        Args:
            account_number: The account number to query
            
        Returns:
            List of position dictionaries
        """
        if not self.session_token:
            print("Not authenticated. Please authenticate first.")
            return []
        
        url = f"{self.base_url}/accounts/{account_number}/positions"
        headers = self._update_auth_headers()
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            return data["data"]["items"]
            
        except requests.exceptions.RequestException as e:
            print(f"Failed to get positions: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return []

    def get_order_history(self, account_number: str) -> List[Dict[str, Any]]:
        """Get order history for a specific account
        
        Args:
            account_number: The account number to query
            
        Returns:
            List of order dictionaries
        """
        if not self.session_token:
            print("Not authenticated. Please authenticate first.")
            return []
        
        url = f"{self.base_url}/accounts/{account_number}/orders"
        headers = self._update_auth_headers()
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            return data["data"]["items"]
            
        except requests.exceptions.RequestException as e:
            print(f"Failed to get order history: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return []
    
    def logout(self) -> bool:
        """Logout and invalidate the session token
        
        Returns:
            bool: True if logout was successful
        """
        if not self.session_token:
            print("Not authenticated.")
            return True
        
        url = f"{self.base_url}/sessions"
        headers = self._update_auth_headers()
        
        try:
            response = requests.delete(url, headers=headers)
            response.raise_for_status()
            
            self.session_token = None
            self.remember_token = None
            print("Logout successful!")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"Failed to logout: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return False


def main():
    """Main function to demonstrate TastyTrade API usage"""
    
    # Replace with your TastyTrade credentials
    username = env.USER
    password = env.PWD
    
    # Initialize API client (using certification environment by default)
    api = TastyTradeAPI(username, password, use_prod=True)
    
    # Authenticate
    if not api.authenticate():
        print("Exiting due to authentication failure")
        return
    
    # Get accounts
    accounts = api.get_accounts()
    
    if not accounts:
        print("No accounts found. Exiting.")
        api.logout()
        return
    
    # Use the first account
    account = accounts[0]
    account_number = account["account"]["account-number"]
    print(f"\nUsing account: {account_number}")
    
    # Get account balances
    balances = api.get_account_balances(account_number)
    print("\nAccount Balances:")
    print(f"Buying Power: ${balances.get('buying-power', 'N/A')}")
    print(f"Cash Balance: ${balances.get('cash-balance', 'N/A')}")
    print(f"Net Liquidating Value: ${balances.get('net-liquidating-value', 'N/A')}")
    
    # Get quotes for some popular stocks
    symbols = ["AAPL", "MSFT", "GOOGL"]
    quotes = api.get_quote(symbols)
    
    print("\nCurrent Quotes:")
    for quote in quotes:
        symbol = quote.get("symbol")
        last_price = quote.get("last-price")
        bid = quote.get("bid-price")
        ask = quote.get("ask-price")
        print(f"{symbol}: Last: ${last_price}, Bid: ${bid}, Ask: ${ask}")
    
    # Get option chains for a symbol
    option_chains = api.get_option_chains("AAPL")
    print(f"\nRetrieved option data with {len(option_chains)} expirations for AAPL")
    
    # Get positions
    positions = api.get_positions(account_number)
    print("\nCurrent Positions:")
    if positions:
        for position in positions:
            symbol = position.get("symbol")
            quantity = position.get("quantity")
            cost_basis = position.get("cost-basis")
            print(f"{symbol}: Quantity: {quantity}, Cost Basis: ${cost_basis}")
    else:
        print("No positions found")
    
    # Get order history
    orders = api.get_order_history(account_number)
    print(f"\nFound {len(orders)} orders in history")
    
    # Note: Uncommenting the following will place a real order!
    # Simulated order placement (commented out for safety)
    '''
    order_response = api.place_equity_order(
        account_number=account_number,
        symbol="AAPL",
        quantity=1,
        order_type="Limit",
        price=150.00,
        side="Buy",
        time_in_force="Day"
    )
    
    if order_response:
        order_id = order_response.get("order", {}).get("id")
        print(f"Order placed with ID: {order_id}")
    '''
    
    # Logout
    api.logout()
    print("\nAPI demonstration completed")


if __name__ == "__main__":
    main()
