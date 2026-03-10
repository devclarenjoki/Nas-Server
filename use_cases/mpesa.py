from domain.mpesa_services import MpesaService

class MpesaUseCase:
    
    @staticmethod
    async def stk_push(phone: str, amount: float, account_reference: str = "EXAMPLE"):
        """
        Public method to trigger STK Push.
        Corresponds to `stkFun` in the JS code.
        """
        if not phone or not amount:
            return {"error": "Missing required values"}, 400
            
        try:
            result = await MpesaService.initiate_stk_push(phone, amount, account_reference)
            print(result)
            return result, 200
        except Exception as e:
            return {"error": str(e)}, 500