# A03 The Magnificent Seven: ændringer i v2 (8. oktober 2026)

Kilder: crit/08_magnificent_critique_1.txt og crit/08_magnificent_critique_3.txt (ingen version 2). Version 3 vægter mest (score 9,0/10). Bemærk: v3-reviewer skriver selv, at MD-filen ikke åbnede, og at reviewet bygger på en tidligere læsning.

## (a) Hovedpåstand før og efter
- **Før:** Begge koncentrations-fortællinger fejlede; "Concentration at two-fifths is a risk to be sized, not a timing signal"; index fund er den billigste måde ikke at misse vinderne.
- **Efter:** I 2012–2026 underperformede de ti største ikke (de slog resten med +5,7% pr. 12 mdr., mest efter 2019), og stigende koncentration forudsagde ikke et equal-weight comeback (svag test); formuedannelsen var ekstremt koncentreret. Det taler imod koncentration som timing-signal, men viser ikke, at koncentration er ufarlig.

## (b) Kritikpunkter der er taget med
- v1+v3: A03-2 formuleret som "ingen målbar evidens for catch-up", ikke evidens imod (lav power fremhævet).
- v1+v3: Eksplicit at artiklen ikke viser, at koncentration ikke er en risiko (abstract, afsnit 5 og 6).
- v1+v3: Konklusionen strammet efter evidensstyrke (tæt på v3's forslag).
- v3 prio 1 og 4 (koncentrations-ladder og benchmark): Top 1/5/10/21/50-andele af formuedannelsen som deskriptiv tabel, plus "Top 1,3% af navnene skabte 39%" og en benchmark-boks med Bessembinder (2018) og forbehold om sammenlignelighed.
- v3 prio 5 / v1 prio 7: Formuefundet er rykket op i "In one paragraph".
- v1+v3: Top-10-cutoff og manglende faktor-attribution nævnt som forbehold.
- v3: Ét regime (platform/AI) gjort konkret med split af perioden (se e).
- Egen redigering: År-for-år-tabellen er fjernet (Figure 2 og periodesplittet bærer pointen) for at holde længden nede.

## (c) Kritikpunkter der ikke er taget med
- Ingen afviste i substans. Reviewerens formulering "+5,7% årligt" er ikke overtaget; artiklen bevarer "per 12 months", fordi målet er overlappende 12-måneders spreads, ikke et årligt afkast af en handlet strategi.
- Formuetabellen er ikke flyttet foran de præregistrerede tests (v3 prio 5 "placér efter sektion 3" er allerede tilfældet).

## (d) Analyser kritikken beder om, som IKKE er lavet (kræver ny beregning)
- A03-1 gentaget for top 5, top 20 og top 50 (v1 prio 4, v3 prio 3).
- Lorenz-figur for formuedannelse (v1 prio 2, v3 prio 2) – kun tabel er lavet, ingen ny figur.
- Faktorprofil/attribution af top-10 (kvalitet, profitabilitet, momentum) (v1 prio 6, v3 prio 7).
- Totalafkast inkl. udbytte; længere historik (fx før 2012) for at teste flere regimer.

## (e) Nye deskriptive tal (rapporteret, ikke testet)
- Fra `results/wealth_creation_by_stock.csv` (792 navne, sorteret efter dollar-formue): kumulativ andel af netto-formue for top 1 (7,8%), top 5 (30,2%), top 20 (49,6%), top 21 (≥50%), top 50 (63,8%), top 100 (75,5%). Top 10 (39,5%) og top 16 (46,6%) stemmer med summary.json.
- Fra `results/concentration_monthly.csv` (kolonne `spread`, 163 startmåneder): gennemsnit for startmåneder 2012–2018 +1,1% (59% positive, n 83) og 2019–2025 +10,5% (74% positive, n 80); uden startår 2019 og 2023: +2,4%. Totalgennemsnit +5,7% genfundet.
- "About 14 independent years" = 163 overlappende måneder / 12, som i den oprindelige tekst.
