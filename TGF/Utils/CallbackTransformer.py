class CallbackTransformer():
    separator = '|'
    
    @staticmethod
    def Join(*variants):
        return CallbackTransformer.separator.join(variants)

    def Split(variants):
        return variants.split(CallbackTransformer.separator)

