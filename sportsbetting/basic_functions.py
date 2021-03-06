#!/usr/bin/env python3
"""
Assistant de paris sportifs
"""

from itertools import product
import numpy as np


def gain(cotes, mise=1):
    """
    :param cotes: Cotes au format décimal
    :type cotes: list[float]
    :param mise: Mise à répartir sur toutes les cotes
    :type mise: float
    :return: Gain pour une somme des mises égale à mise
    :rtype: int
    """
    return mise / sum(map(lambda x: 1 / x, cotes))


def gain2(cotes, i, mise=1):
    """
    :param cotes: Cotes au format décimal
    :type cotes: list[float]
    :param i: Indice de la cote sur laquelle miser
    :type i: int
    :param mise: Mise à placer sur une unique issue
    :type mise: float
    :return: Plus-value générée
    :rtype: float
    """
    return cotes[i] * mise - sum(mises2(cotes, mise, i))


def mises(cotes, mise=1, output=False):
    """
    :param cotes: Cotes au format décimal
    :type cotes: list[float]
    :param mise: Mise à répartir sur toutes les cotes
    :param output: Affichage des détails
    :type output: bool
    :return: Répartition optimale des mises
    :rtype: list[float] or None
    """
    gains = gain(cotes, mise)
    mises_reelles = list(map(lambda x: gains / x, cotes))
    if output:
        mis = list(map(lambda x: round(x, 2), mises_reelles))
        print("somme des mises =", round(sum(mis), 2))
        print("gain min =", min([round(mis[i] * cotes[i], 2)
                                 for i in range(len(mis))]))
        print("gain max =", max([round(mis[i] * cotes[i], 2)
                                 for i in range(len(mis))]))
        print("plus-value max =",
              round(min([round(mis[i] * cotes[i], 2)
                         for i in range(len(mis))]) - sum(mis), 2))
        print("mises arrondies =", mis)
        return
    return mises_reelles


def mises2(cotes, mise_requise, choix=-1, output=False):
    """
    Calcule la repartition des mises en pariant mise_requise sur l'une des
    issues. Par défaut, mise_requise est placée sur la cote la plus basse.

    :param cotes: Cotes au format décimal
    :type cotes: list[float]
    :param mise_requise: Mise à répartir sur toutes les cotes
    :type mise_requise: float
    :param choix: Indice de la cote sur laquelle miser
    :type choix: int
    :param output: Affichage des détails
    :type output: bool
    :return: Répartition optimale des mises
    :rtype: list[float] or None
    """
    if choix == -1:
        choix = np.argmin(cotes)
    gains = mise_requise * cotes[choix]
    mises_reelles = list(map(lambda x: gains / x, cotes))
    if output:
        mis = list(map(lambda x: round(x, 2), mises_reelles))
        print("somme des mises =", round(sum(mis), 2))
        print("gain min =", min([round(mis[i] * cotes[i], 2)
                                 for i in range(len(mis))]))
        print("gain max =", max([round(mis[i] * cotes[i], 2)
                                 for i in range(len(mis))]))
        print("plus-value min =",
              round(min([round(mis[i] * cotes[i], 2)
                         for i in range(len(mis))]) - sum(mis), 2))
        print("plus-value max =",
              round(max([round(mis[i] * cotes[i], 2)
                         for i in range(len(mis))]) - sum(mis), 2))
        print("mises arrondies =", mis)
        return
    return mises_reelles


def cotes_freebet(cotes):
    """
    Calcule les cotes d'un match joué avec des paris gratuits

    :param cotes: Cotes au format décimal
    :type cotes: list[float]
    :return: Cotes réduites de 1
    :rtype: list[float]
    """
    return list(map(lambda x: (x - 1 if x > 1 else 0.01), cotes))


def mises_freebets(cotes, mise):
    """
    Calcule la repartition des mises en paris gratuits pour maximiser les gains
    avec une mise totale égale à mise
    :param cotes:
    :type cotes:
    :param mise:
    :type mise:
    :return:
    :rtype:

    """
    return mises(cotes_freebet(cotes), mise)


def mises_freebet(cotes, freebet, issue=-1, output=False):
    """
    Calcule la repartition des mises en presence d'un freebet a placer sur l'une
    des issues. Par defaut, le freebet est place sur la cote la plus haute.
    """
    if issue == -1:
        issue = np.argmax(cotes)
    mises_reelles = mises2(cotes[:issue] + [cotes[issue] - 1] + cotes[issue + 1:], freebet, issue)
    gains = mises_reelles[issue] * (cotes[issue] - 1)
    if output:
        mis = list(map(lambda x: round(x, 2), mises_reelles))
        print("gain sur freebet =", round(gains + freebet - sum(mis), 2))
        print("gain sur freebet / mise freebet =", round(gains + freebet - sum(mis), 2) / freebet)
        print("gain =", round(gains, 2))
        print("mise totale (hors freebet) =", round(sum(mis) - freebet, 2))
        print("mises arrondies =", mis)
        return
    return mises_reelles


def mises_freebet2(cotes, freebet, issue=-1, output=False):
    """
    Calcule la repartition des mises en presence de 2 freebets a placer sur des issues d'un même
    match. Le 2e freebet est placé automatiquement.
    """
    i_max = np.argmax(cotes)
    if issue == -1:
        issue = i_max
    mises_reelles = mises2(cotes[:issue] + [cotes[issue] - 1] + cotes[issue + 1:], freebet, issue)
    gains = mises_reelles[issue] * (cotes[issue] - 1)
    issue2 = int(np.argmax(cotes[:i_max] + [0] + cotes[i_max + 1:]) if issue == i_max else i_max)
    mis = list(map(lambda x: round(x, 2), mises_reelles))
    rapport_gain = (gains + freebet - sum(mis)) / freebet
    if rapport_gain < (cotes[issue2] - 1) / cotes[issue2]:
        mises_reelles[issue2] = round(gains / (cotes[issue2] - 1), 2)
        mis = list(map(lambda x: round(x, 2), mises_reelles))
        freebet += mis[issue2]
    if output:
        print("gain sur freebet =", round(gains + freebet - sum(mis), 2))
        print("gain sur freebet / mise freebet =", round(gains + freebet - sum(mis), 2) / freebet)
        print("gain =", round(gains, 2))
        print("mise totale (hors freebet) =", round(sum(mis) - freebet, 2))
        print("mises arrondies =", mis)
        return issue2
    return mises_reelles


def gain_freebet2(cotes, freebet, issue=-1):
    """
    Calcule le taux de gain si l'on place deux freebets sur un match même match.
    """
    i_max = np.argmax(cotes)
    if issue == -1:
        issue = i_max
    mises_reelles = mises2(cotes[:issue] + [cotes[issue] - 1] + cotes[issue + 1:], freebet, issue)
    gains = mises_reelles[issue] * (cotes[issue] - 1)
    issue2 = int(np.argmax(cotes[:i_max] + cotes[i_max + 1:]) if issue == i_max else i_max)
    mis = list(map(lambda x: round(x, 2), mises_reelles))
    rapport_gain = (gains + freebet - sum(mis)) / freebet
    if rapport_gain < (cotes[issue2] - 1) / cotes[issue2]:
        mis[issue2] = round(gains / (cotes[issue2] - 1), 2)
        freebet += mis[issue2]
    return (gains + freebet - sum(mis)) / freebet


def cotes_combine(cotes):
    """
    Calcule les cotes de plusieurs matches combines
    """
    out = []
    res = list(product(*cotes))
    for i in res:
        out.append(round(float(np.prod(i)), 4))
    return out


def gain_pari_rembourse_si_perdant(cotes, mise_max, rang=-1, remb_freebet=False,
                                   taux_remboursement=1):
    """
    Calcule le bénéfice lorsque l'un des paris est rembourse. Par
    defaut, la mise remboursee est placee sur la cote la plus haute et le
    remboursement est effectue en argent reel
    """
    taux = ((not remb_freebet) + 0.77 * remb_freebet) * taux_remboursement
    if rang == -1:
        rang = np.argmax(cotes)
    gains = mise_max * cotes[rang]
    mis = list(map(lambda x: (gains - mise_max * taux) / x, cotes))
    mis[rang] = mise_max
    return gains - sum(mis)


def mises_pari_rembourse_si_perdant(cotes, mise_max, rang=-1, remb_freebet=False,
                                    taux_remboursement=1, output=False):
    """
    Calcule les mises lorsque l'un des paris est rembourse. Par
    defaut, la mise remboursee est placee sur la cote la plus haute et le
    remboursement est effectue en argent reel
    """
    taux = ((not remb_freebet) + 0.77 * remb_freebet) * taux_remboursement
    if rang == -1:
        rang = np.argmax(cotes)
    gains = mise_max * cotes[rang]
    mis_reelles = list(map(lambda x: (gains - mise_max * taux) / x, cotes))
    mis_reelles[rang] = mise_max
    if output:
        mis = list(map(lambda x: round(x, 2), mis_reelles))
        print("gain net =", round(gains - sum(mis), 2))
        print("mises arrondies =", mis)
        return
    return mis_reelles


def mises_promo_gain_cote(cotes, mise_minimale, rang, output=False):
    """
    Calcule la répartition des mises pour la promotion "gain en freebet de la cote gagnée"
    """
    mis = []
    gains = cotes[rang] * 0.77 + mise_minimale * cotes[rang]
    for cote in cotes:
        mis.append((gains / cote))
    mis[rang] = mise_minimale
    if output:
        print("somme mises=", sum(mis))
        print("gain=", gains)
    return mis


def gain_promo_gain_cote(cotes, mise_minimale, rang):
    """
    Calcule le gain pour la promotion "gain en freebet de la cote gagnée"
    """
    mis = []
    gains = cotes[rang] * 0.77 + mise_minimale * cotes[rang]
    for cote in cotes:
        mis.append((gains / cote))
    mis[rang] = mise_minimale
    return gains - sum(mis)


def cote_boostee(cote, boost_selon_cote=True, freebet=True, boost=1):
    """
    Calcul de cote boostee pour promotion Betclic
    """
    mult_freebet = 1 * (not freebet) + 0.8 * freebet
    if not boost_selon_cote:
        return cote + (cote - 1) * boost * mult_freebet
    if cote < 2:
        return cote
    if cote < 2.51:
        return cote + (cote - 1) * 0.25 * mult_freebet
    if cote < 3.51:
        return cote + (cote - 1) * 0.5 * mult_freebet
    return cote + (cote - 1) * mult_freebet


def taux_boost(cote, boost_selon_cote=True, boost=1):
    """
    Calcul du taux de boost pour promotion Betclic
    """
    if not boost_selon_cote:
        return boost
    if cote < 2:
        return 0
    if cote < 2.51:
        return 0.25
    if cote < 3.51:
        return 0.5
    return 1


def mises_gains_nets_boostes(cotes, gain_max, boost_selon_cote=True, freebet=True, boost=1, output=False):
    """
    Optimisation de gain pour promotion Betclic de type "Cotes boostees"
    """
    new_cotes = list(map(lambda x: cote_boostee(x, boost_selon_cote, freebet, boost), cotes))
    benefice_max = -float("inf")
    meilleures_mises = []
    for i, cote in enumerate(cotes):
        if not taux_boost(cote, boost_selon_cote, boost):
            continue
        mise = gain_max / ((cotes[i] - 1) * taux_boost(cote, boost_selon_cote, boost))
        mises_possibles = mises2(new_cotes, mise, i)
        mises_corrigees = []
        benefice = 0
        for j, mis in enumerate(mises_possibles):
            if mis * ((cotes[j] - 1) * taux_boost(cotes[j], boost_selon_cote, boost)) > gain_max + 0.1:
                mises_corrigees.append(mise * cote / cotes[j])
            else:
                mises_corrigees.append(mis)
                benefice = mises_corrigees[j] * new_cotes[j]
        benefice -= sum(mises_corrigees)
        if benefice > benefice_max:
            benefice_max = benefice
            meilleures_mises = mises_corrigees
    if output:
        print("somme des mises =", sum(meilleures_mises))
        print("plus-value =", round(benefice_max, 2))
    return meilleures_mises


def gain_gains_nets_boostes(cotes, gain_max, boost_selon_cote=True, freebet=True, boost=1):
    """
    Optimisation de gain pour promotion Betclic de type "Cotes boostees"
    """
    new_cotes = list(map(lambda x: cote_boostee(x, boost_selon_cote, freebet, boost), cotes))
    benefice_max = -float("inf")
    for i, cote in enumerate(cotes):
        mise = gain_max / ((cotes[i] - 1) * taux_boost(cote, boost_selon_cote, boost))
        mises_possibles = mises2(new_cotes, mise, i)
        mises_corrigees = []
        benefice = 0
        for j, mis in enumerate(mises_possibles):
            if mis * ((cotes[j] - 1) * taux_boost(cotes[j], boost_selon_cote, boost)) > gain_max + 0.1:
                mises_corrigees.append(mise * cote / cotes[j])
            else:
                mises_corrigees.append(mis)
                benefice = mises_corrigees[j] * new_cotes[j]
        benefice -= sum(mises_corrigees)
        if benefice > benefice_max:
            benefice_max = benefice
    return benefice_max


def paris_rembourses_si_perdants(cotes, remboursement_max, freebet, taux_remboursement):
    """
    Calcule les mises à placer lorsque tous les paris perdants sont remboursés
    """
    rg_max = int(np.argmax(cotes))
    n = len(cotes)
    facteur = (1 - 0.2 * freebet) * taux_remboursement
    systeme = []
    for i, cote in enumerate(cotes):
        line = [facteur for _ in range(n + 1)]
        line[-1] = -1
        line[i] = cote
        systeme.append(line)
    line = [taux_remboursement for _ in range(n + 1)]
    line[rg_max] = 0
    line[-1] = 0
    systeme.append(line)
    a = np.array(systeme)
    values = [0 for _ in range(n + 1)]
    values[-1] = remboursement_max
    b = np.array(values)
    x = np.linalg.solve(a, b)
    print("Bénéfice net:", x[-1] - sum(x[:-1]))
    print(x[:-1])


def mises_pari_rembourse_si_perdant_paliers(cotes, output=False):
    """
    Optimisation de la promotion Zebet qui attribue un unique cashback en fonction de la plus haute
    mise perdue
    """

    def aux(mise):
        if mise > 25:
            return 10
        elif mise > 20:
            return 8
        elif mise > 15:
            return 6
        elif mise > 10:
            return 4
        elif mise > 5:
            return 2
        else:
            return 0

    sorted_cotes = sorted(cotes)
    mise_max = 25.01
    gain_approx = mise_max * sorted_cotes[0]
    retour_approx = aux(gain_approx / sorted_cotes[1])
    gains = gain_approx + retour_approx * 0.8
    while aux((gains - aux(mise_max) * 0.8) / sorted_cotes[1]) != retour_approx:
        retour_approx -= 2
        gains = gain_approx + retour_approx
    mis_reelles = []
    for cote in cotes:
        mis_reelles.append((gains - aux(mise_max) * 0.8) / cote)
    mis_reelles[int(np.argmin(cotes))] = mise_max
    if output:
        mis = list(map(lambda x: round(x, 2), mis_reelles))
        print("gain net =", gains - sum(mis))
        print("mises arrondies =", mis)
        return
    return mis_reelles
