from typing import Tuple, Dict, List
from collections import defaultdict  # noqa
from .langs import langs
from ...user_functions import (
    capitalize,
    century,
    extract_keywords_from,
    italic,
    strong,
    term,
)


def render_acronyme(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_acronyme("acronyme", ["fr"], defaultdict(str))
    '<i>(Acronyme)</i>'
    >>> render_acronyme("acronyme", ["en"], defaultdict(str, {"de":"light-emitting diode", "m":"oui"}))
    'Acronyme de <i>light-emitting diode</i>'
    >>> render_acronyme("acronyme", ["en"], defaultdict(str, {"de":"light-emitting diode"}))
    'acronyme de <i>light-emitting diode</i>'
    >>> render_acronyme("acronyme", ["en", "fr"], defaultdict(str, {"de":"light-emitting diode", "texte":"Light-Emitting Diode", "m":"1" }))
    'Acronyme de <i>Light-Emitting Diode</i>'
    """  # noqa
    if not data["texte"] and not data["de"]:
        return italic("(Acronyme)")
    phrase = "Acronyme" if data["m"] in ("1", "oui") else "acronyme"
    return f"{phrase} de {italic(data['texte'] or data['de'])}"


def render_agglutination(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_agglutination("agglutination", [], defaultdict(str, {"m":"1"}))
    'Agglutination'
    >>> render_agglutination("agglutination", ["fr"], defaultdict(str, {"de":"harbin", "texte":"l'harbin", "m":"1"}))
    "Agglutination de <i>l'harbin</i>"

    >>> render_agglutination("dénominal", [], defaultdict(str))
    'dénominal'
    >>> render_agglutination("dénominal",[], defaultdict(str, {"de":"psychoanalyze", "m":"1"}))
    'Dénominal de <i>psychoanalyze</i>'

    >>> render_agglutination("déverbal", [], defaultdict(str))
    'déverbal'
    >>> render_agglutination("déverbal", [], defaultdict(str, {"de":"peko", "lang":"eo", "m":"0"}))
    'déverbal de <i>peko</i>'
    >>> render_agglutination("déverbal", [], defaultdict(str, {"de":"accueillir", "m":"1"}))
    'Déverbal de <i>accueillir</i>'
    >>> render_agglutination("déverbal sans suffixe", [], defaultdict(str, {"de":"réserver", "m":"1"}))
    'Déverbal sans suffixe de <i>réserver</i>'

    >>> render_agglutination("syncope", ["fr"], defaultdict(str, { "m":"1"}))
    'Syncope'
    >>> render_agglutination("syncope", ["fr"], defaultdict(str, {"de":"ne voilà-t-il pas"}))
    'syncope de <i>ne voilà-t-il pas</i>'
    >>> render_agglutination("parataxe", ["fr"], defaultdict(str, {"de":"administrateur", "de2":"réseau"}))
    'parataxe de <i>administrateur</i> et de <i>réseau</i>'
    >>> render_agglutination("déglutination", ["fr"], defaultdict(str, {"de":"agriote", "texte":"l’agriote", "m":"1"}))
    'Déglutination de <i>l’agriote</i>'

    >>> render_agglutination("univerbation", ["fr"], defaultdict(str, {"m":"1", "de":"gens", "de2":"armes"}))
    'Univerbation de <i>gens</i> et de <i>armes</i>'
    >>> render_agglutination("univerbation", ["fr"], defaultdict(str, {"m":"1", "de":"gens", "texte":"les gens", "de2":"armes", "texte2":"les armes"}))
    'Univerbation de <i>les gens</i> et de <i>les armes</i>'
    """  # noqa
    phrase = tpl
    if data["m"] == "1":
        phrase = capitalize(phrase)

    if data["de"]:
        phrase += " de "
        if data["nolien"] != "1" and data["texte"]:
            phrase += italic(data["texte"])
        else:
            phrase += italic(data["de"])

    if tpl in ("univerbation", "parataxe") and data["de2"]:
        phrase += " et de "
        if data["nolien"] != "1" and data["texte2"]:
            phrase += italic(data["texte2"])
        else:
            phrase += italic(data["de2"])
    return phrase


def render_argot(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_argot("argot", ["fr"], defaultdict(str))
    '<i>(Argot)</i>'
    >>> render_argot("argot", ["fr", "militaire"], defaultdict(str))
    '<i>(Argot militaire)</i>'
    >>> render_argot("argot", ["argot", "fr"], defaultdict(str, {"spéc":"militaire"}))
    '<i>(Argot militaire)</i>'
    """
    phrase = "Argot"
    if data["spéc"]:
        phrase += f" {data['spéc']}"
    elif len(parts) == 2:
        phrase += f" {parts[1]}"
    return term(phrase)


def render_cit_ref(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_cit_ref("cit_réf", ["Dictionnaire quelconque", "2007"], defaultdict(str))
    '<i>Dictionnaire quelconque</i>, 2007'
    >>> render_cit_ref("cit_réf", [], defaultdict(str,{"titre":"Dictionnaire quelconque", "date":"2007"}))
    '<i>Dictionnaire quelconque</i>, 2007'
    >>> render_cit_ref("cit_réf", ["Dictionnaire quelconque"], defaultdict(str, {"date":"2007"}))
    '<i>Dictionnaire quelconque</i>, 2007'
    >>> render_cit_ref("cit_réf", ["Dictionnaire quelconque", "2007", "Certain auteur"], defaultdict(str))
    'Certain auteur, <i>Dictionnaire quelconque</i>, 2007'
    >>> render_cit_ref("cit_réf", ["Dictionnaire quelconque", "2007", "Certain auteur", "Certain article"], defaultdict(str))
    '«&nbsp;Certain article&nbsp;», dans Certain auteur, <i>Dictionnaire quelconque</i>, 2007'
    >>> render_cit_ref("cit_réf", ["2007"], defaultdict(str, {"titre":"Dictionnaire quelconque", "auteur":"Certain auteur", "article":"Certain article"}))
    '«&nbsp;Certain article&nbsp;», dans Certain auteur, <i>Dictionnaire quelconque</i>, 2007'
    >>> render_cit_ref("cit_réf", ["Nephilologus", "1934"], defaultdict(str, {"auteur_article":"Marius", "article":"Certain article", "pages":"pp. 241-259"}))
    'Marius, «&nbsp;Certain article&nbsp;», dans <i>Nephilologus</i>, 1934, pp. 241-259'
    """  # noqa
    i = 0
    if data["titre"]:
        phrase = italic(data["titre"])
    else:
        phrase = italic(parts[i])
        i += 1
    phrase += ", "
    if data["date"]:
        phrase += data["date"]
    elif i < len(parts):
        phrase += parts[i]
        i += 1
    if data["auteur"]:
        phrase = data["auteur"] + ", " + phrase
    elif i < len(parts):
        phrase = parts[i] + ", " + phrase
        i += 1
    if data["article"]:
        phrase = f"«&nbsp;{data['article']}&nbsp;», dans {phrase}"
    elif i < len(parts):
        phrase = f"«&nbsp;{parts[i]}&nbsp;», dans {phrase}"
        i += 1
    phrase += f", {data['pages']}" if data["pages"] else ""
    phrase = f"{data['auteur_article']}, {phrase}" if data["auteur_article"] else phrase
    return phrase


def render_compose_de(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_compose_de("composé de", ["longus", "aevum"], defaultdict(str, {"lang":"la"}))
    'composé de <i>longus</i> et de <i>aevum</i>'
    >>> render_compose_de("composé de", ["longus", "aevum"], defaultdict(str, {"lang":"la", "f":"1"}))
    'composée de <i>longus</i> et de <i>aevum</i>'
    >>> render_compose_de("composé de", ["longus", "aevum"], defaultdict(str, {"sens1":"long", "sens2":"temps", "lang":"la", "m":"1"}))
    'Composé de <i>longus</i> («&nbsp;long&nbsp;») et de <i>aevum</i> («&nbsp;temps&nbsp;»)'
    >>> render_compose_de("composé de", ["longus", "aevum"], defaultdict(str, {"sens":"long temps", "lang":"la"}))
    'composé de <i>longus</i> et de <i>aevum</i>, littéralement «&nbsp;long temps&nbsp;»'
    >>> render_compose_de("composé de", ["δῆμος", "ἀγωγός"], defaultdict(str, {"tr1":"dêmos", "sens1":"peuple", "tr2":"agōgós", "sens2":"guide", "sens":"celui qui guide le peuple", "lang":"grc", "m":"1"}))
    'Composé de δῆμος, <i>dêmos</i> («&nbsp;peuple&nbsp;») et de ἀγωγός, <i>agōgós</i> («&nbsp;guide&nbsp;»), littéralement «&nbsp;celui qui guide le peuple&nbsp;»'
    >>> render_compose_de("composé de", ["aux", "mains", "de"], defaultdict(str, {"m":"1"}))
    'Composé de <i>aux</i>, <i>mains</i> et de <i>de</i>'
    >>> render_compose_de("composé de", ["anti-", "quark"], defaultdict(str, {"lang":"en"}))
    'dérivé de <i>quark</i> avec le préfixe <i>anti-</i>'
    >>> render_compose_de("composé de", ["anti-", "quark"], defaultdict(str, {"sens":"quarks au rebut"}))
    'dérivé de <i>quark</i> avec le préfixe <i>anti-</i>, littéralement «&nbsp;quarks au rebut&nbsp;»'
    >>> render_compose_de("composé de", ["anti-", "quark"], defaultdict(str, {"lang":"en", "m":"1", "f":"1"}))
    'Dérivée de <i>quark</i> avec le préfixe <i>anti-</i>'
    >>> render_compose_de("composé de", ["clear", "-ly"], defaultdict(str, {"lang":"en", "m":"1"}))
    'Dérivé de <i>clear</i> avec le suffixe <i>-ly</i>'
    >>> render_compose_de("composé de", ["느낌", "표"], defaultdict(str, {"tr1":"neukkim", "sens1":"sensation", "tr2":"-pyo", "sens2":"symbole", "lang":"ko", "m":"1"}))
    'Dérivé de 느낌, <i>neukkim</i> («&nbsp;sensation&nbsp;») avec le suffixe 표, <i>-pyo</i> («&nbsp;symbole&nbsp;»)'
    """  # noqa
    is_derived = any(part.startswith("-") or part.endswith("-") for part in parts)
    is_derived |= any(
        part.startswith("-") or part.endswith("-") for part in data.values()
    )

    if is_derived:
        # Dérivé
        phrase = "D" if "m" in data else "d"
        phrase += "érivée de " if "f" in data else "érivé de "

        parts = sorted(parts, key=lambda part: "-" in part)

        multiple = len(parts) > 2
        for number, part in enumerate(parts, 1):
            is_prefix = part.endswith("-") or data.get(f"tr{number}", "").endswith("-")
            is_suffix = part.startswith("-") or data.get(f"tr{number}", "").startswith(
                "-"
            )
            phrase += "préfixe " if is_prefix else "suffixe " if is_suffix else ""

            phrase += f"{part}" if f"tr{number}" in data else f"{italic(part)}"
            if f"tr{number}" in data:
                idx = f"tr{number}"
                phrase += f", {italic(data[idx])}"
            if f"sens{number}" in data:
                idx = f"sens{number}"
                phrase += f" («&nbsp;{data[idx]}&nbsp;»)"

            phrase += (
                " avec le "
                if number == len(parts) - 1
                else ", "
                if multiple and number <= len(part)
                else ""
            )

        if "sens" in data:
            phrase += f", littéralement «&nbsp;{data['sens']}&nbsp;»"

        return phrase

    # Composé
    phrase = "C" if "m" in data else "c"
    phrase += "omposée de " if "f" in data else "omposé de "
    multiple = len(parts) > 2
    for number, part in enumerate(parts, 1):
        phrase += f"{part}" if f"tr{number}" in data else f"{italic(part)}"
        if f"tr{number}" in data:
            idx = f"tr{number}"
            phrase += f", {italic(data[idx])}"
        if f"sens{number}" in data:
            idx = f"sens{number}"
            phrase += f" («&nbsp;{data[idx]}&nbsp;»)"

        phrase += (
            " et de "
            if number == len(parts) - 1
            else ", "
            if multiple and number <= len(part)
            else ""
        )

    if "sens" in data:
        phrase += f", littéralement «&nbsp;{data['sens']}&nbsp;»"

    return phrase


def render_date(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_date("date", [""], defaultdict(str))
    '<i>(Date à préciser)</i>'
    >>> render_date("date", ["?"], defaultdict(str))
    '<i>(Date à préciser)</i>'
    >>> render_date("date", [], defaultdict(str))
    '<i>(Date à préciser)</i>'
    >>> render_date("date", ["1957"], defaultdict(str))
    '<i>(1957)</i>'
    >>> render_date("date", ["vers l'an V"], defaultdict(str))
    "<i>(Vers l'an V)</i>"
    """
    date = parts[-1] if parts and parts[-1] not in ("", "?") else "Date à préciser"
    return term(capitalize(date))


def render_equiv_pour(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_equiv_pour("équiv-pour", ["un homme", "maître"], defaultdict(str))
    '<i>(pour un homme on dit</i>&nbsp: maître<i>)</i>'
    >>> render_equiv_pour("équiv-pour", ["le mâle", "lion"], defaultdict(str))
    '<i>(pour le mâle on dit</i>&nbsp: lion<i>)</i>'
    >>> render_equiv_pour("équiv-pour", ["une femme", "autrice", "auteure", "auteuse"], defaultdict(str))
    '<i>(pour une femme on peut dire</i>&nbsp: autrice, auteure, auteuse<i>)</i>'
    >>> render_equiv_pour("équiv-pour", ["une femme", "professeure", "professeuse", "professoresse", "professrice"], defaultdict(str, {"texte":"certains disent"}))
    '<i>(pour une femme certains disent</i>&nbsp: professeure, professeuse, professoresse, professrice<i>)</i>'
    """  # noqa
    phrase = f"(pour {parts.pop(0)} "
    phrase += data.get("texte", "on dit" if len(parts) == 1 else "on peut dire")
    return f"{italic(phrase)}&nbsp: {', '.join(parts)}{italic(')')}"


def render_etyl(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_etyl("calque", ["la", "fr"], defaultdict(str))
    'latin'
    >>> render_etyl("calque", ["en", "fr"], defaultdict(str, {"mot":"to date", "sens":"à ce jour"}))
    'anglais <i>to date</i> («&nbsp;à ce jour&nbsp;»)'
    >>> render_etyl("calque", ["sa", "fr"], defaultdict(str, {"mot":"वज्रयान", "tr":"vajrayāna", "sens":"véhicule du diamant"}))
    'sanskrit वज्रयान, <i>vajrayāna</i> («&nbsp;véhicule du diamant&nbsp;»)'
    >>> render_etyl("étyl", ["grc", "fr"], defaultdict(str))
    'grec ancien'
    >>> render_etyl("étyl", ["la", "fr", "dithyrambicus"], defaultdict(str))
    'latin <i>dithyrambicus</i>'
    >>> render_etyl("étyl", ["no", "fr"], defaultdict(str, {"mot":"ski"}))
    'norvégien <i>ski</i>'
    >>> render_etyl("étyl", ["la", "fr"], defaultdict(str, {"mot":"invito", "type":"verb"}))
    'latin <i>invito</i>'
    >>> render_etyl("étyl", ["grc", "fr"], defaultdict(str, {"mot":"λόγος", "tr":"lógos", "type":"nom", "sens":"étude"}))
    'grec ancien λόγος, <i>lógos</i> («&nbsp;étude&nbsp;»)'
    >>> render_etyl("étyl", ["grc", "fr", "λόγος", "lógos", "étude"], defaultdict(str, {"type":"nom", "lien":"1"}))
    'grec ancien λόγος, <i>lógos</i> («&nbsp;étude&nbsp;»)'
    >>> render_etyl("étyl", ["la", "fr"], defaultdict(str, {"mot":"jugulum", "sens":"endroit où le cou se joint aux épaules = la gorge"}))  # noqa
    'latin <i>jugulum</i> («&nbsp;endroit où le cou se joint aux épaules = la gorge&nbsp;»)'
    >>> render_etyl("étyl", ["la", "fr", "tr"], defaultdict(str, {"mot":"subgrunda", "sens":"même sens"}))
    'latin <i>subgrunda</i> («&nbsp;même sens&nbsp;»)'
    >>> render_etyl("étyl", ["grc", "fr"], defaultdict(str, {"mot":""}))
    'grec ancien'
    >>> render_etyl('étyl', ['grc'], defaultdict(str, {"mot":"ὑπόθεσις", "tr":"hupóthesis", "sens":"action de mettre dessous", "nocat":"1"}))
    'grec ancien ὑπόθεσις, <i>hupóthesis</i> («&nbsp;action de mettre dessous&nbsp;»)'
    >>> render_etyl("étyl", ["grc", "fr"], defaultdict(str, {"tr":"leipein", "sens":"abandonner"}))
    'grec ancien <i>leipein</i> («&nbsp;abandonner&nbsp;»)'
    >>> render_etyl("étyl", [], defaultdict(str, {"1":"grc", "2":"es", "mot":"νακτός", "tr":"naktós", "sens":"dense"}))
    'grec ancien νακτός, <i>naktós</i> («&nbsp;dense&nbsp;»)'
    >>> render_etyl("étyl", ["proto-indo-européen", "fr"], defaultdict(str))
    'indo-européen commun'
    >>> render_etyl("étylp", ["la", "fr"], defaultdict(str, {"mot":"Ladon"}))
    'latin <i>Ladon</i>'
    """
    # The lang name
    phrase = langs[data["1"] or parts.pop(0)]
    for part in parts:
        if part in langs:
            continue
        if not data["mot"]:
            data["mot"] = part
        elif not data["tr"]:
            data["tr"] = part
        elif not data["sens"]:
            data["sens"] = part
    if data["tr"]:
        if data["mot"]:
            phrase += f" {data['mot']},"
        phrase += f" {italic(data['tr'])}"
    elif data["mot"]:
        phrase += f" {italic(data['mot'])}"
    if data["sens"]:
        phrase += f" («&nbsp;{data['sens']}&nbsp;»)"
    return phrase


def render_la_verb(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_la_verb("la-verb", ["amō", "amare", "amāre", "amavi", "amāvi", "amatum", "amātum"], defaultdict(str))
    '<b>amō</b>, <i>infinitif</i> : amāre, <i>parfait</i> : amāvi, <i>supin</i> : amātum'
    >>> render_la_verb("la-verb", ["vŏlo", "velle", "velle", "volui", "vŏlŭi"], defaultdict(str, {"2ps":"vis", "2ps2":"vīs", "pattern":"irrégulier"}))
    '<b>vŏlo</b>, vīs, <i>infinitif</i> : velle, <i>parfait</i> : vŏlŭi <i>(irrégulier)</i>'
    >>> render_la_verb("la-verb", ["horrĕo", "horrere", "horrēre", "horrui", "horrŭi"], defaultdict(str, {"pattern":"sans passif"}))
    '<b>horrĕo</b>, <i>infinitif</i> : horrēre, <i>parfait</i> : horrŭi <i>(sans passif)</i>'
    >>> render_la_verb("la-verb", ["sum", "es", "esse", "esse", "fui", "fui", "futurus", "futurus"], defaultdict(str, {"2ps":"es", "2ps2":"es", "pattern":"irrégulier", "44":"participe futur"}))
    '<b>sum</b>, es, <i>infinitif</i> : esse, <i>parfait</i> : fui, <i>participe futur</i> : futurus <i>(irrégulier)</i>'
    """  # noqa
    phrase = strong(parts[0]) + ","
    if data["2ps"]:
        phrase += f" {data.get('2ps2', data['2ps'])},"
    phrase += f" {italic('infinitif')} : {parts[2]}"
    if parts[3] != "-":
        phrase += f", {italic('parfait')} : {parts[4]}"
    if data["44"]:
        phrase += f", {italic(data['44'])} : {parts[6]}"
    elif len(parts) > 5:
        phrase += f", {italic('supin')} : {parts[6]}"
    if data["pattern"]:
        phrase += " " + italic(f"({data['pattern']})")
    return phrase


def render_lien(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_lien("l", ["dies Lunae", "la"], defaultdict(str))
    'dies Lunae'
    >>> render_lien("lien", ["渦", "zh-Hans"], defaultdict(str))
    '渦'
    >>> render_lien("lien", ["フランス", "ja"], defaultdict(str, {"sens":"France"}))
    'フランス («&nbsp;France&nbsp;»)'
    >>> render_lien("lien", ["フランス", "ja"], defaultdict(str, {"tr":"Furansu", "sens":"France"}))
    'フランス, <i>Furansu</i> («&nbsp;France&nbsp;»)'
    >>> render_lien("lien", ["camara", "la"], defaultdict(str, {"sens":"voute, plafond vouté"}))
    'camara («&nbsp;voute, plafond vouté&nbsp;»)'
    """
    phrase = parts.pop(0)
    if data["tr"]:
        phrase += f", {italic(data['tr'])}"
    if data["sens"]:
        phrase += f" («&nbsp;{data['sens']}&nbsp;»)"
    return phrase


def render_lien_rouge(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_lien_rouge("LienRouge", [], defaultdict(str, {"fr":"Comité", "trad":"United Nations", "texte":"COPUOS"}))
    '<i>COPUOS</i>'
    >>> render_lien_rouge("LienRouge", ["Comité"], defaultdict(str, {"trad":"Ausschuss", "texte":"COPUOS"}))
    '<i>COPUOS</i>'
    >>> render_lien_rouge("LienRouge", [], defaultdict(str, {"fr":"Comité", "trad":"United Nations"}))
    '<i>Comité</i>'
    >>> render_lien_rouge("LienRouge", ["Comité"], defaultdict(str, {"trad":"Ausschuss"}))
    '<i>Comité</i>'
    >>> render_lien_rouge("LienRouge", [], defaultdict(str, {"fr":"Comité"}))
    '<i>Comité</i>'
    >>> render_lien_rouge("LienRouge", ["Comité"], defaultdict(str))
    '<i>Comité</i>'
    >>> render_lien_rouge("LienRouge", [], defaultdict(str, {"trad":"United Nations"}))
    '<i>United Nations</i>'
    """
    res = ""
    if data["texte"]:
        res = italic(data["texte"])
    elif data["fr"]:
        res = italic(data["fr"])
    elif parts:
        res = italic(parts[0])
    elif data["trad"]:
        res = italic(data["trad"])
    return res


def render_polytonique(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_polytonique("polytonique", ["μηρóς", "mêrós", "cuisse"], defaultdict(str))
    'μηρóς, <i>mêrós</i> («&nbsp;cuisse&nbsp;»)'
    >>> render_polytonique("polytonique", ["φόβος", "phóbos"], defaultdict(str, {"sens":"effroi, peur"}))
    'φόβος, <i>phóbos</i> («&nbsp;effroi, peur&nbsp;»)'
    >>> render_polytonique("Polytonique",["नामन्", "nā́man"], defaultdict(str))
    'नामन्, <i>nā́man</i>'
    >>> render_polytonique("Polytonique", ["هند", "hend", "Inde"], defaultdict(str))
    'هند, <i>hend</i> («&nbsp;Inde&nbsp;»)'
    """
    phrase = parts.pop(0)
    if data["tr"] or parts:
        phrase += f", {italic(data['tr'] or parts.pop(0))}"
    if data["sens"] or parts:
        phrase += f" («&nbsp;{data['sens'] or parts.pop(0)}&nbsp;»)"
    return phrase


def render_recons(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_recons("recons", ["maruos"], defaultdict(str))
    '*<i>maruos</i>'
    >>> render_recons("recons", ["maruos", "gaul"], defaultdict(str))
    '*<i>maruos</i>'
    >>> render_recons("recons", ["maruos", "gaul"], defaultdict(str, {"sens":"mort"}))
    '*<i>maruos</i> («&nbsp;mort&nbsp;»)'
    >>> render_recons("recons", ["sporo"], defaultdict(str, {"lang-mot-vedette":"fr", "sc":"Latn"}))
    '*<i>sporo</i>'
    >>> render_recons("recons", [], defaultdict(str, {"lang-mot-vedette":"fr"}))
    '*'
    """
    phrase = italic(parts.pop(0)) if parts else ""
    if data["sens"]:
        phrase += f" («&nbsp;{data['sens']}&nbsp;»)"
    return f"*{phrase}"


def render_siecle(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_siecle("siècle", [], defaultdict(str))
    '<i>(Siècle à préciser)</i>'
    >>> render_siecle("siècle", ["?"], defaultdict(str))
    '<i>(Siècle à préciser)</i>'
    >>> render_siecle("siècle", [""], defaultdict(str))
    '<i>(Siècle à préciser)</i>'
    >>> render_siecle("siècle", ["XVIII"], defaultdict(str))
    '<i>(XVIII<sup>e</sup> siècle)</i>'
    >>> render_siecle("siècle", ["XVIII"], defaultdict(str))
    '<i>(XVIII<sup>e</sup> siècle)</i>'
    >>> render_siecle("siècle", ["XVIII", "XIX"], defaultdict(str))
    '<i>(XVIII<sup>e</sup> siècle - XIX<sup>e</sup> siècle)</i>'
    """
    parts = [part for part in parts if part.strip() and part not in ("lang=fr", "?")]
    phrase = century(parts, "siècle") if parts else "Siècle à préciser"
    return term(phrase)


def render_suisse(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_suisse("Suisse", ["fr"], defaultdict(str, {"précision":"Fribourg, Valais, Vaud"}))
    '<i>(Suisse : Fribourg, Valais, Vaud)</i>'
    >>> render_suisse("Suisse", ["it"], defaultdict(str))
    '<i>(Suisse)</i>'
    """
    if data["précision"]:
        return term(f"Suisse : {data['précision']}")
    else:
        return term("Suisse")


def render_suppletion(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_suppletion("supplétion", ["aller"], defaultdict(str))
    'Cette forme dénote une supplétion car son étymologie est distincte de celle de <i>aller</i>'
    >>> render_suppletion("supplétion", ["un"], defaultdict(str, {"mot":"oui"}))
    'Ce mot dénote une supplétion car son étymologie est distincte de celle de <i>un</i>'
    >>> render_suppletion("supplétion", ["better", "best"], defaultdict(str, {"lang":"en", "mot":"oui"}))
    'Ce mot dénote une supplétion car son étymologie est distincte de celles de <i>better</i> et de <i>best</i>'
    >>> render_suppletion("supplétion", ["am", "are", "was"], defaultdict(str, {"lang":"en", "mot":"oui"}))
    'Ce mot dénote une supplétion car son étymologie est distincte de celles de <i>am</i>, de <i>are</i> et de <i>was</i>'
    """  # noqa
    if data["mot"]:
        phrase = "Ce mot dénote une supplétion car son étymologie est distincte de "
    else:
        phrase = (
            "Cette forme dénote une supplétion car son étymologie est distincte de "
        )
    if len(parts) > 1:
        phrase += "celles de "
        phrase += ", de ".join(f"{italic(p)}" for p in parts[:-1])
        phrase += f" et de {italic(parts[-1])}"
    else:
        phrase += f"celle de {italic(parts[0])}"
    return phrase


def render_zh_lien(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_zh_lien("zh-lien", ["人", "rén"], defaultdict(str))
    '人 (<i>rén</i>)'
    >>> render_zh_lien("zh-lien", ["马", "mǎ", "馬"], defaultdict(str))
    '马 (馬, <i>mǎ</i>)'
    >>> render_zh_lien("zh-lien", ["骨", "gǔ", "骨"], defaultdict(str))
    '骨 (骨, <i>gǔ</i>)'
    """
    simple = parts.pop(0)
    pinyin = italic(parts.pop(0))
    traditional = parts[0] if parts else ""
    if not traditional:
        return f"{simple} ({pinyin})"
    return f"{simple} ({traditional}, {pinyin})"


template_mapping = {
    "acronyme": render_acronyme,
    "agglutination": render_agglutination,
    "argot": render_argot,
    "calque": render_etyl,
    "cit_réf": render_cit_ref,
    "cit réf": render_cit_ref,
    "composé de": render_compose_de,
    "composé_de": render_compose_de,
    "date": render_date,
    "déglutination": render_agglutination,
    "dénominal": render_agglutination,
    "déverbal": render_agglutination,
    "déverbal sans suffixe": render_agglutination,
    "équiv-pour": render_equiv_pour,
    "étyl": render_etyl,
    "étylp": render_etyl,
    "forme reconstruite": render_recons,
    "la-verb": render_la_verb,
    "lien": render_lien,
    "l": render_lien,
    "LienRouge": render_lien_rouge,
    "parataxe": render_agglutination,
    "polytonique": render_polytonique,
    "Polytonique": render_polytonique,
    "recons": render_recons,
    "reverlanisation": render_agglutination,
    "siècle": render_siecle,
    "Suisse": render_suisse,
    "supplétion": render_suppletion,
    "syncope": render_agglutination,
    "univerbation": render_agglutination,
    "zh-lien": render_zh_lien,
}


def lookup_template(tpl: str) -> bool:
    return tpl in template_mapping


def render_template(template: Tuple[str, ...]) -> str:
    tpl, *parts = template
    data = extract_keywords_from(parts)
    return template_mapping[tpl](tpl, parts, data)