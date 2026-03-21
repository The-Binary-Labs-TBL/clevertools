from __future__ import annotations

from clevertools import mask
from typing import TypedDict
import pytest

from ._debug import debug

class MaskVisibilityOptions(TypedDict, total=False):
    show_start_characters: int
    show_end_characters: int

PASSWORD_CASES = (
    (
        "symbols_one",
        "<;t#(bTj&e=ygJ<y;u*6xf?>7pd^s06YVw#t.2]e%URufAXm(GAraZwAwUgd.!;g",
        "<;t#(bTj******************************************************;g",
    ),
    (
        "symbols_two",
        "BW1yJ0wd?y7bXc!9WDfW*auwXbkFth*%waGaJVNt2gQZ3304H=s[Mjq8<Gu2yyBR",
        "BW1yJ0wd******************************************************BR",
    ),
    (
        "symbols_three",
        "hE9vVF>%sjtr%CTp$F#.YuUwu]BvYm%59xWPwWk5=T@w@RY1MbD**ukw*Ke!]#J1",
        "hE9vVF>%******************************************************J1",
    ),
    (
        "symbols_four",
        "j=&Q:XttwDa+PQ5+TgEtdCFNr$tH+&kXVuZT[1rsC$syrt.XRQQ22vDH@>PuNR$E",
        "j=&Q:Xtt******************************************************$E",
    ),
    (
        "words_one",
        "embellish-geologic-sanding-patriarch-crank-transform",
        "embellis******************************************rm",
    ),
    (
        "words_two",
        "handwash-clapped-tripping-arose-brilliant-unbeaten",
        "handwash****************************************en",
    ),
    (
        "words_three",
        "snuff-film-script-overstock-latticed-muck",
        "snuff-fi*******************************ck",
    ),
    (
        "words_four",
        "geiger-sleet-jasmine-antiques-ipod-steam",
        "geiger-s******************************am",
    ),
)

CUSTOM_MASK_CASES = (
    (
        "symbols_one_custom",
        "<;t#(bTj&e=ygJ<y;u*6xf?>7pd^s06YVw#t.2]e%URufAXm(GAraZwAwUgd.!;g",
        {"show_start_characters": 5, "show_end_characters": 10},
        "<;t#(*************************************************wAwUgd.!;g",
    ),
    (
        "symbols_two_custom",
        "BW1yJ0wd?y7bXc!9WDfW*auwXbkFth*%waGaJVNt2gQZ3304H=s[Mjq8<Gu2yyBR",
        {"show_start_characters": 1, "show_end_characters": 1},
        "B**************************************************************R",
    ),
    (
        "symbols_three_custom",
        "hE9vVF>%sjtr%CTp$F#.YuUwu]BvYm%59xWPwWk5=T@w@RY1MbD**ukw*Ke!]#J1",
        {"show_start_characters": 2, "show_end_characters": 20},
        "hE******************************************@RY1MbD**ukw*Ke!]#J1",
    ),
    (
        "symbols_four_custom",
        "j=&Q:XttwDa+PQ5+TgEtdCFNr$tH+&kXVuZT[1rsC$syrt.XRQQ22vDH@>PuNR$E",
        {"show_start_characters": 6, "show_end_characters": 3},
        "j=&Q:X*******************************************************R$E",
    ),
    (
        "words_one_custom",
        "embellish-geologic-sanding-patriarch-crank-transform",
        {"show_start_characters": 9, "show_end_characters": 2},
        "embellish*****************************************rm",
    ),
    (
        "words_two_custom",
        "handwash-clapped-tripping-arose-brilliant-unbeaten",
        {"show_start_characters": 123, "show_end_characters": 12},
        "handwash-clapped-tripping-arose-brill*ant-unbeaten",
    ),
    (
        "words_three_custom",
        "snuff-film-script-overstock-latticed-muck",
        {"show_start_characters": 1231312, "show_end_characters": 131231},
        "*nuff-film-script-overstock-latticed-muck",
    ),
    (
        "words_four_custom",
        "geiger-sleet-jasmine-antiques-ipod-steam",
        {"show_start_characters": 12, "show_end_characters": 25},
        "geiger-sleet***smine-antiques-ipod-steam",
    ),
)


class MaskTestBase:
    def _assert_mask(
        self,
        secret: str,
        expected: str,
        *,
        show_start_characters: int | None = None,
        show_end_characters: int | None = None,
        mask_character: str = "*",
    ) -> None:
        masked = mask(
            secret,
            show_start_characters=show_start_characters,
            show_end_characters=show_end_characters,
            mask_character=mask_character,
            on_error="raise",
        )
        debug(f"Maskiere Wert: {secret}")
        debug(f"Maskiertes Ergebnis: {masked}")
        assert masked == expected


class TestMaskHandlerDefaults(MaskTestBase):
    @pytest.mark.parametrize(("label", "secret", "expected"), PASSWORD_CASES)
    def test_default_masking_matches_expected_output(
        self,
        label: str,
        secret: str,
        expected: str,
    ) -> None:
        debug(f"Pruefe Standard-Masking fuer {label}.")
        self._assert_mask(secret, expected)

    def test_mask_uses_expected_defaults(self) -> None:
        debug("Pruefe den dokumentierten Default-Maskierungswert.")
        self._assert_mask("1234567890ABCDEF", "12345678******EF")


class TestMaskHandlerCustomVisibility(MaskTestBase):
    @pytest.mark.parametrize(("label", "secret", "kwargs", "expected"), CUSTOM_MASK_CASES)
    def test_custom_masking_matches_expected_output(
        self,
        label: str,
        secret: str,
        kwargs: MaskVisibilityOptions,
        expected: str,
    ) -> None:
        debug(f"Pruefe benutzerdefiniertes Masking fuer {label}.")
        self._assert_mask(
            secret,
            expected,
            show_start_characters=kwargs.get("show_start_characters"),
            show_end_characters=kwargs.get("show_end_characters"),
        )


class TestMaskHandlerHardening(MaskTestBase):
    def test_mask_rejects_negative_visible_prefix(self) -> None:
        debug("Pruefe Fehlerfall fuer negativen Prefix beim Maskieren.")
        masked = mask("abcdef", show_start_characters=-1, on_error="silent")
        debug(f"Rueckgabewert bei negativem Prefix: {masked!r}")

        assert masked == ""

    def test_mask_rejects_negative_visible_suffix(self) -> None:
        debug("Pruefe Fehlerfall fuer negativen Suffix beim Maskieren.")
        masked = mask("abcdef", show_end_characters=-1, on_error="silent")
        debug(f"Rueckgabewert bei negativem Suffix: {masked!r}")

        assert masked == ""

    def test_mask_rejects_invalid_mask_character(self) -> None:
        debug("Pruefe Fehlerfall fuer ein ungueltiges mask_character.")
        masked = mask("abcdef", mask_character="XX", on_error="silent")
        debug(f"Rueckgabewert bei ungueltigem mask_character: {masked!r}")

        assert masked == ""

    def test_mask_rejects_empty_values(self) -> None:
        debug("Pruefe Fehlerfall fuer leere Eingaben.")
        masked = mask("", on_error="silent")
        debug(f"Rueckgabewert bei leerem Wert: {masked!r}")

        assert masked == ""

    def test_mask_rejects_non_string_values(self) -> None:
        debug("Pruefe Fehlerfall fuer Nicht-String-Eingaben.")
        masked = mask(123456, on_error="silent")  # type: ignore[arg-type]
        debug(f"Rueckgabewert bei Nicht-String-Wert: {masked!r}")

        assert masked == ""

    def test_mask_supports_custom_mask_character_exactly(self) -> None:
        debug("Pruefe exakte Ausgabe mit benutzerdefiniertem Maskierungszeichen.")
        self._assert_mask(
            "ABCDEFGHIJKL",
            "ABCD######KL",
            show_start_characters=4,
            show_end_characters=2,
            mask_character="#",
        )

    def test_mask_masks_single_character_values_consistently(self) -> None:
        debug("Pruefe Grenzfall fuer einen einzelnen Charakter.")
        self._assert_mask("A", "*")

    def test_mask_raises_for_invalid_mask_character_in_raise_mode(self) -> None:
        with pytest.raises(ValueError, match="mask_character must be exactly one character"):
            mask("abcdef", mask_character="XX", on_error="raise")