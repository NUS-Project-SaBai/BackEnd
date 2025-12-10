from typing import TypedDict


class VitalsRegistrationAPIData(TypedDict):
    temperature: str

    # Children vitals
    scoliosis: str
    pallor: str

    # Puberty
    pubarche: str
    pubarche_age: str
    thelarche: str
    thelarche_age: str
    menarche_age: str
    voice_change: str
    voice_change_age: str
    testicular_growth: str
    testicular_growth_age: str
