"""Hydroqc custom types."""

# pylint: disable=invalid-name
from typing import TypedDict


class DTDataResultsTyping(TypedDict, total=True):
    """DT winter period data (legacy format)."""

    dateDebut: str
    dateFin: str
    dateDernMaj: str
    hrsCritiquesAppelee: str
    hrsCritiquesAppeleesMax: str
    montantEconPerteVSTarifBase: float
    nbJoursTotauxHiver: int
    nbJoursDernMaj: int
    etatHiver: str


class DTDataTyping(TypedDict, total=True):
    """FlexD data json output format."""

    success: bool
    results: list[DTDataResultsTyping]
