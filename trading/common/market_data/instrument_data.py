class InstrumentData:
    nse_instruments: dict = None
    nfo_instruments: dict = None

    @classmethod
    def get_token_from_nfo_instrument(cls, instrument_symbol: str) -> int:
        if instrument_symbol not in cls.nfo_instruments:
            return None

        return cls.nfo_instruments[instrument_symbol]['instrument_token']
