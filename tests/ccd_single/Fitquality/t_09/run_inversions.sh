#!/usr/bin/env sh
rm -r results_*

ccd_single --output_format ascii -o results_ascii --plot --norm 10
ccd_single --output_format ascii_audit -o results_ascii_audit --plot --norm 10

DD_COND=1 ccd_single --output_format ascii -o results_cond_ascii --plot --norm 10
DD_COND=1 ccd_single --output_format ascii_audit -o results_cond_ascii_audit --plot --norm 10

