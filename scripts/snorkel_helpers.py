from snorkel.labeling import LabelingFunction
from ast import literal_eval

ABSTAIN = -1

############ Functions, that are simple keyword search ###########

# https://www.snorkel.org/use-cases/01-spam-tutorial 

def keyword_lookup(x, keywords, label):
     for keyword in keywords:
        if keyword.lower() in x.clean_text.lower():
            return label
        else:
            return ABSTAIN


def make_keyword_lf(keywords, label, name):
    return LabelingFunction(
        name=name,
        f=keyword_lookup,
        resources=dict(keywords=keywords, label=label),
    )

############ Functions, that are list lookup ###########

def list_lookup(x, keywords, label, lf_type):
    if bool(set(literal_eval(x[lf_type])) & set(keywords)):
        return label
    else:
        return ABSTAIN


def make_list_lookup_lf(keywords, label, name, lf_type):
    return LabelingFunction(
        name=name,
        f=list_lookup,
        resources=dict(keywords=keywords, label=label, lf_type=lf_type),
    )