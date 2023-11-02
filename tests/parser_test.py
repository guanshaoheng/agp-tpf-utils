import io
import pytest
import re

from textwrap import dedent

from tola.assembly.parser import parse_agp, parse_tpf

def	test_parse_agp():
    # Careful using auto-formatters on this code which may strip tab
    # characters from this test AGP!
    agp = strip_leading_spaces(
        """
        ##agp-version 2.1
        #
        # DESCRIPTION: Generated by PretextView Version 0.2.5
        # HiC MAP RESOLUTION: 8666.611572 bp/texel

        Scaffold_1	1	21337197	1	W	scaffold_1	1	21337197	+	Painted
        Scaffold_1	21337198	21337297	2	U	100	scaffold	yes	proximity_ligation
        Scaffold_1	21337298	21917959	3	W	scaffold_21	1	580662	+
        Scaffold_1	21917960	21918059	4	U	100	scaffold	yes	proximity_ligation
        Scaffold_1	21918060	24379376	5	W	scaffold_1	21770529	24231845	-	Painted
        Scaffold_2	1	3206646	1	W	scaffold_2	1	3206646	+	Painted
        Scaffold_2	3206647	3206746	2	U	100	scaffold	yes	proximity_ligation
        Scaffold_2	3206747	3267412	3	W	scaffold_67	1	60666	+	Painted
        Scaffold_2	3267413	3267512	4	U	100	scaffold	yes	proximity_ligation
        Scaffold_2	3267513	28348686	5	W	scaffold_2	3206647	28287820	?	Painted
        """
    )

    fh = io.StringIO(agp)
    a1 = parse_agp(fh, "aaBbbCccc1")
    assert str(a1) == strip_leading_spaces(
        """
        Assembly: aaBbbCccc1
          # DESCRIPTION: Generated by PretextView Version 0.2.5
          # HiC MAP RESOLUTION: 8666.611572 bp/texel
          Scaffold_1
                      1    21337197  scaffold_1:1-21337197(+) Painted
               21337198    21337297  Gap:100 scaffold
               21337298    21917959  scaffold_21:1-580662(+)
               21917960    21918059  Gap:100 scaffold
               21918060    24379376  scaffold_1:21770529-24231845(-) Painted
          Scaffold_2
                      1     3206646  scaffold_2:1-3206646(+) Painted
                3206647     3206746  Gap:100 scaffold
                3206747     3267412  scaffold_67:1-60666(+) Painted
                3267413     3267512  Gap:100 scaffold
                3267513    28348686  scaffold_2:3206647-28287820(.) Painted
        """
    )

def	test_parse_tpf():
    with pytest.raises(
        ValueError, match=r"Gap line before first sequence fragment"
    ):
        parse_tpf(io.StringIO("GAP	TYPE-2	200"), "gap_first")

    with pytest.raises(ValueError, match=r"Unexpected name format"):
        parse_tpf(
            io.StringIO("?	frag	scaffold_1	PLUS"),
            "bad_fragment_name",
        )

    with pytest.raises(ValueError, match=r"Wrong field count"):
        parse_tpf(
            io.StringIO("?	scaffold_2:166926-629099"),
            "too_few_fields",
        )

    tpf = strip_leading_spaces(
        """
        ?	scaffold_1:1-93024	scaffold_1	PLUS
        GAP	TYPE-2	200
        ?	scaffold_1:93225-232397	scaffold_1	PLUS
        GAP	TYPE-2	200
        ?	scaffold_1:232598-261916	scaffold_1	PLUS
        GAP	TYPE-2	200
        ?	scaffold_1:262117-906261	scaffold_1	PLUS
        ?	scaffold_2:1-166725	scaffold_2	PLUS
        GAP	TYPE-2	200
        ?	scaffold_2:166926-629099	scaffold_2	MINUS
        GAP	TYPE-2	200
        ?	scaffold_2:629300-719848	scaffold_2	MINUS
        GAP	TYPE-2	200
        ?	scaffold_2:720049-3207246	scaffold_2	PLUS
        GAP	TYPE-2	200
        ?	scaffold_2:3207447-3240707	scaffold_2	PLUS
        """
    )
    fh = io.StringIO(tpf)
    a1 = parse_tpf(fh, "aaBbbCccc1")
    assert str(a1) == strip_leading_spaces(
        """
        Assembly: aaBbbCccc1
          scaffold_1
                      1       93024  scaffold_1:1-93024(+)
                  93025       93224  Gap:200 TYPE-2
                  93225      232397  scaffold_1:93225-232397(+)
                 232398      232597  Gap:200 TYPE-2
                 232598      261916  scaffold_1:232598-261916(+)
                 261917      262116  Gap:200 TYPE-2
                 262117      906261  scaffold_1:262117-906261(+)
          scaffold_2
                      1      166725  scaffold_2:1-166725(+)
                 166726      166925  Gap:200 TYPE-2
                 166926      629099  scaffold_2:166926-629099(-)
                 629100      629299  Gap:200 TYPE-2
                 629300      719848  scaffold_2:629300-719848(-)
                 719849      720048  Gap:200 TYPE-2
                 720049     3207246  scaffold_2:720049-3207246(+)
                3207247     3207446  Gap:200 TYPE-2
                3207447     3240707  scaffold_2:3207447-3240707(+)
        """
    )

def strip_leading_spaces(txt):
    """
    Removes leading blank lines and de-indents text, so that the test data in
    this file can be indented to the code.
    """
    return dedent(txt).lstrip()

if	__name__ == '__main__':
    test_parse_agp()
    test_parse_tpf()
