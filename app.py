import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(layout="wide", page_title="V20 Scanner")

st.title("📈 V20 — Operator Activity Scanner")
st.write(
    "Finds stocks with a run of **consecutive green candles (no red candle) totaling a 20%+ move** — "
    "the signature of operator/strong-hand accumulation — then flags it only once price has "
    "**pulled back into that zone** without breaking below it. Buy-on-pullback, not buy-on-breakout."
)
st.caption("Reference examples from Vivek sir's notes: KAYNES, TRENT, JPPOWER, RAJESHEXPO")

# ---------------- VSpartans Stock Universe ----------------
V40 = [
    "BAJAJHLDNG.NS","ABBOTINDIA.NS","AXISBANK.NS","PFIZER.NS","BERGEPAINT.NS","TITAN.NS",
    "HINDUNILVR.NS","BATAINDIA.NS","LT.NS","RELIANCE.NS","MARICO.NS","BAJAJ-AUTO.NS",
    "KOTAKBANK.NS","TCS.NS","DABUR.NS","SBIN.NS","VOLTAS.NS","PGHH.NS","ITC.NS",
    "BAJFINANCE.NS","ICICIBANK.NS","HCLTECH.NS","HDFCBANK.NS","HDFCLIFE.NS","GILLETTE.NS",
    "HAVELLS.NS","COLPAL.NS","PIDILITIND.NS","MARUTI.NS","HDFCAMC.NS","NESTLEIND.NS",
    "ICICIPRULI.NS","ICICIGI.NS","ASIANPAINT.NS","GLAXO.NS","DMART.NS","PAGEIND.NS",
    "INFY.NS","BAJAJFINSV.NS"
]

V40_NEXT = [
    "CDSL.NS","BSE.NS","JIOFIN.NS","ANGELONE.NS","CAMS.NS","MCX.NS","ULTRACEMCO.NS","ACC.NS",
    "TEAMLEASE.NS","ASTRAZEN.NS","CIPLA.NS","ERIS.NS","LALPATHLAB.NS","APOLLOHOSP.NS",
    "MEDANTA.NS","FORTIS.NS","ADANIPORTS.NS","JSWINFRA.NS","AWL.NS","GODREJCP.NS","DIXON.NS",
    "KAJARIACER.NS","HONAUT.NS","DMART.NS","RELAXO.NS","BLUESTARCO.NS","BOSCHLTD.NS",
    "EICHERMOT.NS","MRF.NS","M&M.NS","TATAMOTORS.NS","HYUNDAI.NS","INDHOTEL.NS","ITCHOTELS.NS",
    "UNITDSPR.NS","RADICO.NS","UBL.NS","VBL.NS"
]

V200 = [
    "VOLTAMP.NS","GPIL.NS","POLYCAB.NS","INGERRAND.NS","J&KBANK.NS","KTKBANK.NS","RPGLIFE.NS",
    "MSUMI.NS","NIITMTS.NS","CMSINFO.NS","TANLA.NS","GPPL.NS","PNB.NS","MARICO.NS",
    "SOUTHBANK.NS","DOMS.NS","EMAMILTD.NS","HCLTECH.NS","CELLO.NS","IEX.NS","ABSLAMC.NS",
    "TI.NS","GRAVITA.NS","UTIAMC.NS","JBCHEPHARM.NS","FORCEMOT.NS","HINDCOPPER.NS","PAGEIND.NS",
    "GROWW.NS","GRSE.NS","TRITURBINE.NS","GODFRYPHLP.NS","ENGINERSIN.NS","NATIONALUM.NS",
    "ZENTEC.NS","DABUR.NS","BLS.NS","NBCC.NS","SCHAEFFLER.NS","RATNAMANI.NS","LICI.NS",
    "CGPOWER.NS","CHAMBLFERT.NS","VESUVIUS.NS","ZFCVINDIA.NS","UNIONBANK.NS","ESABINDIA.NS",
    "GANESHHOU.NS","DBCORP.NS","SUZLON.NS","BAJFINANCE.NS","HEROMOTOCO.NS","BAYERCROP.NS",
    "CUB.NS","ANTHEM.NS","HAL.NS","CAPLIPOINT.NS","JWL.NS","SHARDAMOTR.NS","TIMKEN.NS",
    "MGL.NS","MARUTI.NS","OSWALPUMPS.NS","HYUNDAI.NS","HDFCAMC.NS","PGHH.NS","KIRLOSBROS.NS",
    "MAZDOCK.NS","SKFINDIA.NS","ITC.NS","SUNPHARMA.NS","BALUFORGE.NS","GVT&D.NS","INOXINDIA.NS",
    "ABB.NS","IMFA.NS","KFINTECH.NS","LOTUSDEV.NS","DIVISLAB.NS","KOTAKBANK.NS","CHOLAFIN.NS",
    "CUMMINSIND.NS","EICHERMOT.NS","OFSS.NS","COFORGE.NS","WELCORP.NS","KEI.NS","ACE.NS",
    "SUNTV.NS","BSOFT.NS","AJAXENGG.NS","ABBOTINDIA.NS","MPHASIS.NS","GILLETTE.NS",
    "PETRONET.NS","TDPOWERSYS.NS","PIDILITIND.NS","HINDUNILVR.NS","INDGN.NS","DODLA.NS",
    "AJANTPHARM.NS","KSB.NS","TCI.NS","COCHINSHIP.NS","KARURVYSYA.NS","IDBI.NS","LTIM.NS",
    "MAITHANALL.NS","NESCO.NS","MAHABANK.NS","CERA.NS","BANKINDIA.NS","ICICIGI.NS",
    "INDIANB.NS","IGIL.NS","GRINDWELL.NS","FIVESTAR.NS","CIGNITITEC.NS","MANAPPURAM.NS",
    "GLAXO.NS","APARINDS.NS","CAMS.NS","FIEMIND.NS","HSCL.NS","DRREDDY.NS","AXISBANK.NS",
    "CDSL.NS","SANOFICONR.NS","NMDC.NS","ELECON.NS","MCX.NS","PERSISTENT.NS","EIHOTEL.NS",
    "COROMANDEL.NS","ZENSARTECH.NS","BOSCHLTD.NS","ASIANPAINT.NS","UNITDSPR.NS","GABRIEL.NS",
    "DATAPATTNS.NS","SHAREINDIA.NS","BANKBARODA.NS","PRUDENT.NS","SURYAROSNI.NS","FINEORG.NS",
    "HDFCBANK.NS","TMB.NS","KPITTECH.NS","LTTS.NS","CONCORDBIO.NS","SHRIRAMFIN.NS","3MINDIA.NS",
    "HBLENGINE.NS","BSE.NS","MANINFRA.NS","IRCTC.NS","APLAPOLLO.NS","LTF.NS","NATCOPHARM.NS",
    "M&MFIN.NS","KSCL.NS","BEL.NS","ECLERX.NS","CRISIL.NS","TIINDIA.NS","SBIN.NS",
    "NESTLEIND.NS","WAAREEINDO.NS","SUNDARMFIN.NS","AKZOINDIA.NS","TCS.NS","LALPATHLAB.NS",
    "POLYMED.NS","SBICARD.NS","TATAELXSI.NS","TRAVELFOOD.NS","PACEDIGITK.NS","MUTHOOTFIN.NS",
    "COLPAL.NS","GHCL.NS","CIPLA.NS","SUMICHEM.NS","AVANTIFEED.NS","INFY.NS","BLUEJET.NS",
    "VBL.NS","COALINDIA.NS","PIIND.NS","SOLARINDS.NS","WAAREERTL.NS","ENRIN.NS","VINATIORGA.NS",
    "GARFIBRES.NS","HEXT.NS","SHRIPISTON.NS","BERGEPAINT.NS","CSBBANK.NS","CANBK.NS","CLEAN.NS",
    "ANANDRATHI.NS","RITES.NS","IGL.NS","CASTROLIND.NS","NEWGEN.NS","LGEINDIA.NS","TATATECH.NS",
    "PFIZER.NS","INDIAMART.NS","AWL.NS","AUBANK.NS","HAVELLS.NS","SUPREMEIND.NS","MSTCLTD.NS",
    "GRWRHITECH.NS","MARKSANS.NS","BANDHANBNK.NS","SPLPETRO.NS","FEDERALBNK.NS","TENNIND.NS",
    "RAILTEL.NS","VSTIND.NS","DHANUKA.NS","PGHL.NS","CENTRALBK.NS","IOB.NS","ALIVUS.NS",
    "NAM-INDIA.NS","JYOTHYLAB.NS","ICICIBANK.NS","ALKEM.NS"
]

def dedupe(tickers):
    seen, out = set(), []
    for t in tickers:
        if t not in seen:
            seen.add(t)
            out.append(t)
    return out

V40 = dedupe(V40)
V40_NEXT = dedupe(V40_NEXT)
V200 = dedupe(V200)

option = st.selectbox("Select Stock Universe to Scan:", ["V40", "V40 Next", "V200", "Custom Tickers"])
if option == "V40":
    tickers = V40
elif option == "V40 Next":
    tickers = V40_NEXT
elif option == "V200":
    tickers = V200
else:
    symbols_input = st.text_input(
        "Enter Custom Tickers (comma separated)",
        "KAYNES.NS, TRENT.NS, JPPOWER.NS, RAJESHEXPO.NS"
    )
    tickers = [s.strip() for s in symbols_input.split(",") if s.strip()]

st.info(f"Loaded {len(tickers)} stocks for scanning.")

with st.sidebar:
    st.header("Tuning")
    min_zone_gain = st.slider("Minimum zone gain (%)", 15.0, 40.0, 20.0, step=1.0,
                               help="Minimum cumulative move (zone low to zone high) required for a green run to qualify as a V20 zone.")
    lookback_days = st.slider("Lookback period (trading days)", 60, 252, 252,
                               help="How far back to search for V20 zones. 252 ≈ 1 year.")
    max_pullback_overshoot = st.slider("Allow price slightly above zone high (%)", 0.0, 5.0, 0.0, step=0.5,
                                        help="Normally price must have pulled back inside the zone. Raise this to also catch price just above zone high.")

def find_green_runs(df):
    """Split the series into runs of consecutive non-red candles (Close >= Open)."""
    is_green = (df['Close'] >= df['Open']).values
    runs = []
    start = None
    for i, g in enumerate(is_green):
        if g and start is None:
            start = i
        elif not g and start is not None:
            runs.append((start, i - 1))
            start = None
    if start is not None:
        runs.append((start, len(df) - 1))
    return runs

def zone_invalidated(df, end_idx, zone_low):
    """True if price has closed below zone_low at any point after the zone formed."""
    if end_idx + 1 >= len(df):
        return False  # zone just formed, no bars after it yet — not invalidated, but also not a pullback yet
    after = df['Close'].iloc[end_idx + 1:]
    return (after < zone_low).any()

if st.button("Run V20 Scan"):
    results = []
    progress = st.progress(0, text="Starting scan...")

    for n_done, symbol in enumerate(tickers, start=1):
        progress.progress(n_done / len(tickers), text=f"Scanning {symbol}...")
        try:
            stock = yf.Ticker(symbol)
            df = stock.history(period="2y")
            if df.empty or len(df) < 30:
                continue
            df = df.iloc[-lookback_days:].reset_index()

            current_price = df['Close'].iloc[-1]
            runs = find_green_runs(df)

            # Evaluate runs from most recent to oldest; take the first valid, un-invalidated zone
            best_zone = None
            for start_idx, end_idx in reversed(runs):
                zone_low = df['Low'].iloc[start_idx:end_idx+1].min()
                zone_high = df['High'].iloc[start_idx:end_idx+1].max()
                if zone_low <= 0:
                    continue
                zone_gain = ((zone_high - zone_low) / zone_low) * 100
                if zone_gain < min_zone_gain:
                    continue
                # Need at least one bar after the run (the pullback itself) to act on it
                if end_idx >= len(df) - 1:
                    continue
                if zone_invalidated(df, end_idx, zone_low):
                    continue
                best_zone = {
                    "zone_low": zone_low, "zone_high": zone_high, "zone_gain": zone_gain,
                    "start_date": df['Date'].iloc[start_idx].date() if 'Date' in df.columns else None,
                    "end_date": df['Date'].iloc[end_idx].date() if 'Date' in df.columns else None,
                }
                break  # most recent valid zone found

            if best_zone is None:
                continue

            zone_low, zone_high = best_zone["zone_low"], best_zone["zone_high"]
            upper_bound = zone_high * (1 + max_pullback_overshoot / 100)

            # Entry condition: price has pulled back into the zone (or within allowed overshoot),
            # and is not below zone_low (that would mean the zone already failed).
            if not (zone_low <= current_price <= upper_bound):
                continue

            pullback_depth = ((zone_high - current_price) / (zone_high - zone_low)) * 100 if zone_high > zone_low else 0
            target_upside = ((zone_high - current_price) / current_price) * 100

            results.append({
                "Symbol": symbol,
                "Current Price": f"₹{current_price:.2f}",
                "Zone Low": round(zone_low, 2),
                "Zone High": round(zone_high, 2),
                "Zone Gain": f"{best_zone['zone_gain']:.1f}%",
                "Zone Formed": f"{best_zone['start_date']} → {best_zone['end_date']}",
                "Pullback Depth": f"{pullback_depth:.0f}% into zone",
                "Target Upside (Zone High)": f"{target_upside:.1f}%"
            })
        except Exception:
            continue

    progress.empty()

    if results:
        res_df = pd.DataFrame(results)
        st.success(f"Found {len(res_df)} stock(s) currently pulled back into an unbroken V20 zone.")
        st.dataframe(res_df, use_container_width=True)
    else:
        st.info(
            "No stocks currently sitting in a fresh, unbroken V20 zone. Operator-driven runs are "
            "rare by nature — this being empty most days is expected, not a bug."
        )
