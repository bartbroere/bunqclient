def hierarchy():
    return ["avatar", "attachment_public", "installation", "user", 
    "user_person", "user_company", "device", "device_server", "session", 
    "session_server", "server_public_key", "monetary_account", 
    "monetary_account_bank", "payment", "payment_batch", "request_inquiry", 
    "request_inquiry_batch", "request_response", "draft_payment", 
    "schedule_payment", "schedule_payment_batch", "cash_register", 
    "qr_code", "content", "schedule", "schedule_instance", 
    "credential_password_ip", "ip", "tab_usage_single", "tab_usage_multiple", 
    "tab", "tab_item", "tab_item_batch", "qr_code_content", 
    "tab_result_inquiry", "tab_result_response", "mastercard_action", 
    "token_qr_request_ideal", "card", "card_debit", "card_name", "chat", 
    "chat_conversation", "message", "message_attachment", "message_text", 
    "certificate_pinned", "attachment", "attachment_tab", "invoice", 
    "customer_statement", "export_annual_overview", "content"]

def headers():
    return {"Cache-Control": "no-cache",
            "User-Agent": "bunqclient 2017.7.8",
            "X-Bunq-Geolocation": "0 0 0 0 000",
            "X-Bunq-Language": "en_US",
            "X-Bunq-Region": "nl_NL"}