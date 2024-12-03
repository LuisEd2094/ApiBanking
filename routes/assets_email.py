from flask_mail import Message
from app import mail

def send_investment_purchase_confirmation(user, units_purchased, asset_symbol, amount, prices):
 
    msg = Message("Investment Purchase Confirmation", recipients=[user.email])
    msg.body = (f"Dear {user.name},\n\n"
                f"You have successfully purchased {units_purchased:.2f} units of {asset_symbol} for a total amount of ${amount:.2f}.\n\n"
                f"Current holdings of {asset_symbol}: {user.get_asset_quantity(asset_symbol):.2f} units\n\n"
                f"Summary of current assets:\n"
                f"{user.get_current_assets_email()}\n\n"
                f"Account Balance: ${user.balance:.2f}\n"
                f"Net Worth: ${user.get_networth(prices):.2f}\n\n"
                f"Thank you for using our investment services.\n\n"
                f"Best Regards,\n"
                f"Investment Management Team")
    mail.send(msg)

def send_investment_sale_confirmation(user, quantity, asset_symbol, total_gain_loss, total_quantity, prices):
    msg = Message("Investment Sale Confirmation", recipients=[user.email])
    
    msg.body = (f"Dear {user.name},\n\n"
                f"You have successfully sold {quantity:.2f} units of {asset_symbol}.\n\n"
                f"Total Gain/Loss: ${total_gain_loss:.2f}\n"
                f"Remaining holdings of {asset_symbol}: {total_quantity - quantity:.2f} units\n\n"
                f"Summary of current assets:\n"
                f"{user.get_current_assets_email()}\n\n"
                f"Account Balance: ${user.balance:.2f}\n"
                f"Net Worth: ${user.get_networth(prices):.2f}\n\n"
                f"Thank you for using our investment services.\n\n"
                f"Best Regards,\n"
                f"Investment Management Team")
    
    mail.send(msg)