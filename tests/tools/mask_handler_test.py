from __future__ import annotations

from clevertools import mask

passwd_one: str = "<;t#(bTj&e=ygJ<y;u*6xf?>7pd^s06YVw#t.2]e%URufAXm(GAraZwAwUgd.!;g"
passwd_two: str = "BW1yJ0wd?y7bXc!9WDfW*auwXbkFth*%waGaJVNt2gQZ3304H=s[Mjq8<Gu2yyBR"
passwd_three: str = "hE9vVF>%sjtr%CTp$F#.YuUwu]BvYm%59xWPwWk5=T@w@RY1MbD**ukw*Ke!]#J1"
passwd_four: str = "j=&Q:XttwDa+PQ5+TgEtdCFNr$tH+&kXVuZT[1rsC$syrt.XRQQ22vDH@>PuNR$E"

passwd_five: str = "embellish-geologic-sanding-patriarch-crank-transform"
passwd_six: str = "handwash-clapped-tripping-arose-brilliant-unbeaten"
passwd_seven: str = "snuff-film-script-overstock-latticed-muck"
passwd_eight: str = "geiger-sleet-jasmine-antiques-ipod-steam"


class TestMaskHandler:
    def test_default_masking(self) -> None:
        print("=== Masing with clevertools defaults... === \n")

        masked = mask(passwd_one)
        assert masked != passwd_one
        print(f"Masked password one: {masked}")

        masked = mask(passwd_two)
        assert masked != passwd_two
        print(f"Masked password two: {masked}")

        masked = mask(passwd_three)
        assert masked != passwd_three
        print(f"Masked password three: {masked}")

        masked = mask(passwd_four)
        assert masked != passwd_four
        print(f"Masked password four: {masked}")

        masked = mask(passwd_five)
        assert masked != passwd_five
        print(f"Masked password five: {masked}")

        masked = mask(passwd_six)
        assert masked != passwd_six
        print(f"Masked password six: {masked}")

        masked = mask(passwd_seven)
        assert masked != passwd_seven
        print(f"Masked password seven: {masked}")

        masked = mask(passwd_eight)
        assert masked != passwd_eight
        print(f"Masked password eight: {masked}")

    def test_custom_masking(self) -> None:
        print("\n === Masing with clevertools custom values... === \n")

        masked = mask(passwd_one, show_start_characters=5, show_end_characters=10)
        assert masked != passwd_one
        print(f"Masked password one: {masked}")

        masked = mask(passwd_two, show_start_characters=1, show_end_characters=1)
        assert masked != passwd_two
        print(f"Masked password two: {masked}")

        masked = mask(passwd_three, show_start_characters=2, show_end_characters=20)
        assert masked != passwd_three
        print(f"Masked password three: {masked}")

        masked = mask(passwd_four, show_start_characters=6, show_end_characters=3)
        assert masked != passwd_four
        print(f"Masked password four: {masked}")

        masked = mask(passwd_five, show_start_characters=9, show_end_characters=2)
        assert masked != passwd_five
        print(f"Masked password five: {masked}")

        masked = mask(passwd_six, show_start_characters=123, show_end_characters=12)
        assert masked != passwd_six
        print(f"Masked password six: {masked}")

        masked = mask(passwd_seven, show_start_characters=1231312, show_end_characters=131231)
        assert masked != passwd_seven
        print(f"Masked password seven: {masked}")

        masked = mask(passwd_eight, show_start_characters=12, show_end_characters=25)
        assert masked != passwd_eight
        print(f"Masked password eight: {masked}")