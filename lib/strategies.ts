export type Strategy = {
  id: string;
  nameZh: string;
  nameEn: string;
  /** Short description shown on the card (Simplified Chinese). Edit freely. */
  description: string;
  /** Headline KPI label, e.g. "年化回报". */
  kpiLabel: string;
  /** Headline KPI value, e.g. "25%". */
  kpiValue: string;
  /** Optional secondary KPI (e.g. Sharpe, win rate). */
  subKpiLabel?: string;
  subKpiValue?: string;
  /** Tone of headline KPI for color. */
  tone?: 'good' | 'bad' | 'neutral';
  pdfEn?: string;
  pdfZh?: string;
  /** If true, render as a placeholder "coming soon" card. */
  comingSoon?: boolean;
};

export type Category = {
  id: string;
  titleZh: string;
  titleEn: string;
  blurb: string;
  strategies: Strategy[];
};

// Use the basePath at runtime so PDF links work both locally and on GitHub Pages.
const bp = process.env.NEXT_PUBLIC_BASE_PATH || '';
const pdf = (p: string) => `${bp}${p}`;

export const categories: Category[] = [
  {
    id: 'technical',
    titleZh: '技术分析策略',
    titleEn: 'Technical Analysis Strategies',
    blurb: '基于价格行为、形态识别与技术指标构建的系统化交易策略。',
    strategies: [
      {
        id: 'elliott-wave',
        nameZh: '波浪理论动量',
        nameEn: 'Elliott Wave Momentum',
        description: '捕捉第三浪（主升浪）趋势动能，斐波那契精准入场；牛市进攻、熊市空仓，6 年全部正回报，最差年份仅 +0.1%。',
        kpiLabel: '年化回报',
        kpiValue: '16.4%',
        subKpiLabel: '最大回撤',
        subKpiValue: '3.8%',
        tone: 'good',
        pdfEn: pdf('/pdfs/technical/elliott_wave_EN.pdf'),
        pdfZh: pdf('/pdfs/technical/elliott_wave_ZH.pdf'),
      },
      {
        id: 'cup-handle',
        nameZh: '杯柄形态',
        nameEn: 'Cup and Handle',
        description: '5 年回测,0 个亏损年份,最大回撤仅 2.3%。',
        kpiLabel: '近一年回报',
        kpiValue: '25%',
        subKpiLabel: '最大回撤',
        subKpiValue: '2.3%',
        tone: 'good',
        pdfEn: pdf('/pdfs/technical/cup_handle_EN.pdf'),
        pdfZh: pdf('/pdfs/technical/cup_handle_ZH.pdf'),
      },
      {
        id: 'box-theory',
        nameZh: '箱体突破',
        nameEn: 'Box Theory',
        description: '小亏大赢,捕捉横盘整理后的突破机会。',
        kpiLabel: '年化回报',
        kpiValue: '22%',
        tone: 'good',
        pdfEn: pdf('/pdfs/technical/box_theory_EN.pdf'),
        pdfZh: pdf('/pdfs/technical/box_theory_ZH.pdf'),
      },
      {
        id: 'rsi-reversal',
        nameZh: 'RSI 反转',
        nameEn: 'RSI Reversal',
        description: '连续 5 年正回报,通过 RSI 在超买/超卖区间识别反转。',
        kpiLabel: '近一年回报',
        kpiValue: '29%',
        subKpiLabel: '连续盈利',
        subKpiValue: '5 年',
        tone: 'good',
        pdfEn: pdf('/pdfs/technical/rsi_reversal_EN.pdf'),
        pdfZh: pdf('/pdfs/technical/rsi_reversal_ZH.pdf'),
      },
      {
        id: 'btc-lsr',
        nameZh: 'BTC 多空持仓比',
        nameEn: 'BTC Long/Short Ratio',
        description: '近 3 年累计 +125%,最差年份 −5%。',
        kpiLabel: '年化回报',
        kpiValue: '31%',
        subKpiLabel: '3 年累计',
        subKpiValue: '+125%',
        tone: 'good',
        pdfEn: pdf('/pdfs/technical/put_call_ratio_EN.pdf'),
        pdfZh: pdf('/pdfs/technical/put_call_ratio_ZH.pdf'),
      },
    ],
  },
  {
    id: 'onchain',
    titleZh: '链上数据策略',
    titleEn: 'On-Chain Data Strategies',
    blurb: '通过区块链原生数据洞察大额资金动向,先于市场捕捉信号。',
    strategies: [
      {
        id: 'whale-flow',
        nameZh: '鲸鱼资金流向',
        nameEn: 'Exchange Whale Flow',
        description: '追踪交易所大额转入转出,识别巨鲸的建仓与出货行为。5 年累计回报 +338%。',
        kpiLabel: '年化回报',
        kpiValue: '34.5%',
        subKpiLabel: '5 年累计',
        subKpiValue: '+338%',
        tone: 'good',
        pdfEn: pdf('/pdfs/onchain/whale_flow_EN.pdf'),
        pdfZh: pdf('/pdfs/onchain/whale_flow_ZH.pdf'),
      },
      {
        id: 'whale-tracks',
        nameZh: '大户足迹',
        nameEn: 'Whale Tracks',
        description: '读取成交量异动与主动买卖盘 (CVD) 中的大户足迹,在低流通性新币爆发前顺势介入——多由新币上市等事件驱动。CVD 确认方向,顺势持有。覆盖 520+ 币种、两年滚动样本外验证,夏普 ~1.9,最大回撤 ~11%。',
        kpiLabel: '年化回报',
        kpiValue: '120%',
        subKpiLabel: '最大回撤',
        subKpiValue: '11%',
        tone: 'good',
        pdfEn: pdf('/pdfs/onchain/whale_tracks_EN.pdf'),
        pdfZh: pdf('/pdfs/onchain/whale_tracks_ZH.pdf'),
      },
      {
        id: 'onchain-more',
        nameZh: '更多策略即将上线',
        nameEn: 'More to come',
        description: '更多链上数据信号正在研究中。',
        kpiLabel: '',
        kpiValue: '',
        comingSoon: true,
      },
    ],
  },
  {
    id: 'options',
    titleZh: '期权交易策略',
    titleEn: 'Options Trading Strategies',
    blurb: '基于期权定价、波动率结构的衍生品策略。',
    strategies: [
      {
        id: 'btc-deribit',
        nameZh: 'BTC Deribit 期权',
        nameEn: 'BTC Deribit Options',
        description: '在 Deribit 平台上执行 BTC 期权策略,以 BTC 现货积累为目标。含 BTC 自身升值,3 年累计回报 +532%。',
        kpiLabel: '年化回报',
        kpiValue: '94%',
        subKpiLabel: '3 年累计 (含 BTC 升值)',
        subKpiValue: '+532%',
        tone: 'good',
        pdfEn: pdf('/pdfs/options/btc_deribit_EN.pdf'),
        pdfZh: pdf('/pdfs/options/btc_deribit_ZH.pdf'),
      },
    ],
  },
  {
    id: 'dl',
    titleZh: '深度学习策略',
    titleEn: 'Deep Learning Strategies',
    blurb: '利用深度学习模型挖掘非线性特征,构建预测信号。',
    strategies: [
      {
        id: 'dl-more',
        nameZh: '更多策略即将上线',
        nameEn: 'More to come',
        description: '深度学习模型与特征工程正在搭建中。',
        kpiLabel: '',
        kpiValue: '',
        comingSoon: true,
      },
    ],
  },
];
