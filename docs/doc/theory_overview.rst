
Overview
========

.. blockdiag::

    blockdiag sip_models{
        "SIP signature" -> "resistivity formulation";
        "SIP signature" -> "conductivity formulation";
        "resistivity formulation" -> "Cole-Cole model";
        "resistivity formulation" -> "Cole-Cole distribution";
        "Cole-Cole distribution" -> "Debye distribution";
        "Cole-Cole distribution" -> "0 < c <= 1";
        "conductivity formulation" -> "c_cc";
        "conductivity formulation" -> "c_cc_d";
        "c_cc_d" -> "c_dd_d";
        "c_cc_d" -> "c_cc_c";

        "c_cc"[label="Cole-Cole model"];
        "c_cc_d"[label="Cole-Cole distribution"];
        "c_dd_d"[label="Debye distribution"];
        "c_cc_c"[label="c < c <= 1"];
    }
