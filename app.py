import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(layout="wide", page_title="V20 Scanner")

st.title("📈 V20 — Operator Activity Scanner")
st.write(
    "Finds stocks with a run of **consecutive green candles (no red candle) totaling a 20%+ move** — "
    "the signature of operator/strong-hand accumulation — then flags it only once price has "
    "**pulled back into that zone** without breaking below it, **and is currently trading below its "
    "200-day moving average**. Buy-on-pullback, not buy-on-breakout."
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
    "LTM.NS",
    "PGHH.NS","WAAREEINDO.NS","TIPSMUSIC.NS","ICICIAMC.NS","COLPAL.NS","GILLETTE.NS","SANOFICONR.NS",
    "WAAREERTL.NS","NESTLEIND.NS","PGHL.NS","GVPIL.NS","GVT&D.NS","MCX.NS","IGIL.NS",
    "ENRIN.NS","ESABINDIA.NS","PAGEIND.NS","JPOLYINVST.NS","WEBELSOLAR.NS","TCS.NS","GLAXO.NS",
    "TENNIND.NS","CASTROLIND.NS","BSE.NS","HBLENGINE.NS","SANOFI.NS","ANANDRATHI.NS","INGERRAND.NS",
    "CRIZAC.NS","IEX.NS","3MINDIA.NS","CAMS.NS","MARICO.NS","IRCTC.NS","OFSS.NS",
    "ATLANTAELE.NS","EMMVEE.NS","ABBOTINDIA.NS","NAM-INDIA.NS","GRSE.NS","HDFCAMC.NS","HINDCOPPER.NS",
    "TRAVELFOOD.NS","DIXON.NS","GKENERGY.NS","CRAMC.NS","INFY.NS","GLENMARK.NS","NATIONALUM.NS",
    "CUMMINSIND.NS","ITC.NS","MSUMI.NS","WAAREEENER.NS","HYUNDAI.NS","OSWALPUMPS.NS","SOLARINDS.NS",
    "PRUDENT.NS","GROWW.NS","BEL.NS","FORCEMOT.NS","MAZDOCK.NS","SHARDAMOTR.NS","TRITURBINE.NS",
    "HEROMOTOCO.NS","SUZLON.NS","COALINDIA.NS","CHENNPETRO.NS","ECLERX.NS","AJANTPHARM.NS","PERSISTENT.NS",
    "TDPOWERSYS.NS","INOXINDIA.NS","POLYCAB.NS","BBTC.NS","CRISIL.NS","LGEINDIA.NS","ABSLAMC.NS",
    "CDSL.NS","HAL.NS","ACE.NS","APLAPOLLO.NS","ACUTAAS.NS","APARINDS.NS","PIDILITIND.NS",
    "DDEVPLSTIK.NS","NBCC.NS","ENGINERSIN.NS","VIKRAMSOLR.NS","EICHERMOT.NS","HCLTECH.NS","ANTHEM.NS",
    "KIRLPNU.NS","MSTCLTD.NS","GODFRYPHLP.NS","SHARDACROP.NS","HEXT.NS","TATAELXSI.NS","ABB.NS",
    "SKFINDIA.NS","LTIM.NS","POWERINDIA.NS","FIEMIND.NS","BLS.NS","KFINTECH.NS","BAYERCROP.NS",
    "JYOTHYLAB.NS","CPPLUS.NS","HINDUNILVR.NS","RUBICON.NS","VSTIND.NS","RRKABEL.NS","EMAMILTD.NS",
    "GPPL.NS","INDIAMART.NS","LALPATHLAB.NS","STYL.NS","SCHAEFFLER.NS","NMDC.NS","JAMNAAUTO.NS",
    "CGPOWER.NS","LTTS.NS","ASHOKA.NS","BLUEJET.NS","NEULANDLAB.NS","UNITDSPR.NS","ASIANPAINT.NS",
    "TANLA.NS","KPITTECH.NS","GABRIEL.NS","CHAMBLFERT.NS","SUPRIYA.NS","NEWGEN.NS","HAVELLS.NS",
    "KSB.NS","CAPLIPOINT.NS","AVANTIFEED.NS","DOMS.NS","RADICO.NS","PFIZER.NS","QUESS.NS",
    "AJAXENGG.NS","ALIVUS.NS","DHANUKA.NS","MANYAVAR.NS","VOLTAMP.NS","COFORGE.NS","SUMICHEM.NS",
    "KAJARIACER.NS","NSDL.BO","TECHM.NS","RAILTEL.NS","ZENSARTECH.NS","PETRONET.NS","JSWDULUX.NS",
    "BALUFORGE.NS","REFEX.NS","MISHTANN.BO","HSCL.NS","MPHASIS.NS","ELGIEQUIP.NS","COROMANDEL.NS",
    "RITES.NS","BIKAJI.NS","DIVISLAB.NS","DATAPATTNS.NS","ICICIGI.NS","BERGEPAINT.NS","BOSCHLTD.NS",
    "FINEORG.NS","SIEMENS.NS","VESUVIUS.NS","VINATIORGA.NS","WABAG.NS","BLUESTARCO.NS","ALKEM.NS",
    "GRINDWELL.NS","BSOFT.NS","LOTUSDEV.NS","AIAENG.NS","TATATECH.NS","ELECON.NS","SUPREMEIND.NS",
    "EIHOTEL.NS","CLEAN.NS","NIITMTS.NS","SUNPHARMA.NS","AHLUCONT.NS","GPIL.NS","KIRLOSBROS.NS",
    "DABUR.NS","KEI.NS",
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
            df_full = stock.history(period="2y")
            if df_full.empty or len(df_full) < 210:
                continue

            df_full["SMA200"] = df_full["Close"].rolling(window=200).mean()
            dma200 = df_full["SMA200"].iloc[-1]
            current_price_check = df_full["Close"].iloc[-1]
            if pd.isna(dma200):
                continue
            # Core V20 filter: only interested in stocks currently below their 200 DMA
            if current_price_check >= dma200:
                continue

            df = df_full.iloc[-lookback_days:].reset_index()

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
                "200 DMA": f"₹{dma200:.2f}",
                "Below DMA By": f"{((dma200 - current_price) / dma200 * 100):.1f}%",
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
