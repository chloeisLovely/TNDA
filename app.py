import streamlit as st

# --- 페이지 설정 ---
st.set_page_config(
    page_title="EPD 매각 협상 전략 시뮬레이터",
    page_icon="💼",
    layout="centered"
)

# --- 스타일링 (HTML/CSS의 디자인과 유사하게) ---
st.markdown("""
<style>
    .st-emotion-cache-16txtl3 {
        padding-top: 2rem;
    }
    .st-emotion-cache-uf99v8 {
        background-color: #1f2937; /* bg-gray-800 */
        border: 1px solid #374151; /* border-gray-700 */
        border-radius: 0.75rem;
        padding: 1.5rem;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff;
    }
    .st-emotion-cache-1kyxreq {
        justify-content: center;
    }
    .stButton>button {
        background-color: #2563eb; /* bg-blue-600 */
        color: white;
        font-weight: bold;
        padding: 0.75rem 2.5rem;
        border-radius: 0.5rem;
        font-size: 1.125rem;
        transition: all 0.3s;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1d4ed8; /* hover:bg-blue-700 */
        transform: scale(1.05);
    }
    .pro-list { color: #4ade80; } /* green-400 */
    .con-list { color: #f87171; } /* red-400 */
</style>
""", unsafe_allow_html=True)

# --- 앱 제목 및 설명 ---
st.title("EPD 매각 협상 전략 시뮬레이터")
st.markdown("<p style='color:#9ca3af;'>TNDA Corp.의 성공적인 EPD 매각을 위한 최적의 의사결정을 지원합니다.</p>", unsafe_allow_html=True)
st.markdown("---")

# --- 입력 섹션 (2열 레이아웃) ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. 목표 매각가 범위 설정")
    min_price = st.number_input(
        "최소 목표 매각가 (USD)", 
        min_value=0, 
        value=325000000, 
        step=1000000,
        format="%d"
    )
    max_price = st.number_input(
        "최대 목표 매각가 (USD)", 
        min_value=0, 
        value=None, 
        placeholder="상한선 없음",
        step=1000000,
        format="%d"
    )

with col2:
    st.subheader("2. 후보사별 1차 제안가")
    euro_ekv_bid = st.number_input("Euro EKV", min_value=0, value=None, step=1000000, format="%d")
    us_ind_bid = st.number_input("US-IND", min_value=0, value=None, step=1000000, format="%d")
    pearl_equity_bid = st.number_input("Pearl Equity", min_value=0, value=None, step=1000000, format="%d")
    ruby_fibre_bid = st.number_input("RubyFibre", min_value=0, value=None, step=1000000, format="%d")
    
st.markdown("---")

# --- 분석 버튼 ---
if st.button("최적 협상 후보 분석"):
    bidders = [
        {'name': 'Euro EKV', 'bid': euro_ekv_bid, 'type': '전략적 투자자 (SI)', 
         'pros': ['미국 시장 진출 등 강력한 인수 동기', '가장 높은 시너지 프리미엄 지불 가능성', '유럽 시장 지배력 및 기술력 보유'], 
         'cons': ['미국 내 네트워크 부족 가능성']},
        {'name': 'US-IND', 'bid': us_ind_bid, 'type': '전략적 투자자 (SI)', 
         'pros': ['경쟁사 제거 및 시장 점유율 확대 목적', '산업 및 고객 기반에 대한 높은 이해도'], 
         'cons': ['독점 규제 리스크 존재 가능성']},
        {'name': 'Pearl Equity', 'bid': pearl_equity_bid, 'type': '재무적 투자자 (FI)', 
         'pros': ['신속하고 확실한 거래 진행 가능', '풍부한 자금력과 M&A 경험 보유'], 
         'cons': ['가격 상승 잠재력 제한적 (시너지 프리미엄 부재)', '산업에 대한 깊은 이해 부족 가능성']},
        {'name': 'RubyFibre', 'bid': ruby_fibre_bid, 'type': '전략적 투자자 (SI)', 
         'pros': ['기술 및 핵심 인력 확보에 관심'], 
         'cons': ['자금력 부족으로 인한 거래 불확실성 매우 높음', 'M&A 경험 부족']}
    ]

    # None 값을 0으로 처리하여 계산 오류 방지
    for bidder in bidders:
        if bidder['bid'] is None:
            bidder['bid'] = 0

    valid_bidders = [b for b in bidders if b['bid'] > 0 and b['bid'] >= min_price and (max_price is None or max_price == 0 or b['bid'] <= max_price)]
    valid_bidders.sort(key=lambda x: x['bid'], reverse=True)

    st.header("분석 결과 및 전략 제언")

    if not valid_bidders:
        max_price_text = f"~ ${max_price:,}" if max_price and max_price > 0 else "∞"
        st.error(f"**분석 결과: 조건에 맞는 후보 없음**\n\n설정하신 매각가 범위(${min_price:,} {max_price_text})를 충족하는 후보가 없습니다. \n\n매각가 범위를 조정하거나, 각 후보와의 추가 소통이 필요합니다.")
    else:
        st.subheader(f"목표 범위 내 후보사 분석 ({len(valid_bidders)}곳)")
        
        for bidder in valid_bidders:
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{bidder['name']}** <span style='color:#9ca3af;'>({bidder['type']})</span>", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"<p style='text-align: right; color: #4ade80; font-weight: bold; font-size: 1.2rem;'>${bidder['bid']:,}</p>", unsafe_allow_html=True)
                
                pro_con_col1, pro_con_col2 = st.columns(2)
                with pro_con_col1:
                    st.markdown("<h5 class='pro-list'>장점 (Pros)</h5>", unsafe_allow_html=True)
                    for pro in bidder['pros']:
                        st.markdown(f"👍 {pro}")
                with pro_con_col2:
                    st.markdown("<h5 class='con-list'>단점 (Cons)</h5>", unsafe_allow_html=True)
                    for con in bidder['cons']:
                        st.markdown(f"👎 {con}")
        
        st.markdown("---")

        if len(valid_bidders) > 1:
            st.info(
                "**🎯 최종 전략 제언: 2단계 통제된 경매 실행**\n\n"
                f"**1단계 (경쟁 구도 형성):** 현재 범위 내 상위 후보인 **{', '.join([b['name'] for b in valid_bidders[:2]])}** 등을 최종 라운드(본입찰) 후보로 압축하여 경쟁 구도를 명확히 합니다.\n\n"
                "**2단계 (가치 극대화):** 최종 후보들에게만 상세 실사 기회를 제공하고, 각 사의 전략적 목표를 자극하여 최종 가격을 극대화해야 합니다. 강력한 경쟁자들이 존재함을 알려, 최고가 입찰을 유도하는 것이 핵심입니다."
            )
        else:
            st.warning(
                f"**🎯 최종 전략 제언: 단독 협상 전략**\n\n"
                f"유효한 후보가 **{valid_bidders[0]['name']}** 뿐입니다. 경쟁을 통한 가격 상승은 어렵지만, 거래의 확실성은 높습니다. \n\n"
                "협상 시 EPD가 가진 부동산 및 특허의 잠재 가치를 강조하여 제안가를 방어하고, 매각 결렬 시 자체 운영(BATNA) 가능성을 언급하여 협상력을 유지해야 합니다."
            )
