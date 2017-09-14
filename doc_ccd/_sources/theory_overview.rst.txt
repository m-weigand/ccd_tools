
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

Within the scope of this project, the models used to described (i.e. fit) SIP
signatures are divided in formulations using the resistivity and the
conductivity. Within these categories, signatures can either be described by
one term following the Cole-Cole model, or by a superposition of Cole-Cole
terms (i.e. a distribution of Cole-Cole models over the frequency/relaxation
time range). The process of determining the various parameters (weights) for
such a distribution is called a decomposition. The decomposition is then
further subdivided in the Debye decomposition with a fixed *c* value of 1.0,
and the general case for a values of :math:`c \in [0, 1)`. This structure is
mirrored for the conductivity case.

.. toctree::

    theory_helper
