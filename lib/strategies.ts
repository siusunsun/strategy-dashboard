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
  /** Optional overrides for the link button labels and icons (default: "📄 中文报告" / "📄 English"). */
  pdfZhLabel?: string;
  pdfEnLabel?: string;
  pdfZhIcon?: string;
  pdfEnIcon?: string;
  /** Optional link to a live/real-time trading dashboard for this strategy
   *  (rendered as a 实时交易 button on the card). */
  liveDashboardUrl?: string;
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
        id: 'alpha-ta',
        nameZh: '三策略组合',
        nameEn: 'Alpha TA 3-Strategy',
        description: '多种技术分析策略的组合，涵盖技术指标、动量指标与图表形态。',
        kpiLabel: '6 年累计回报',
        kpiValue: '+51.3%',
        subKpiLabel: '最大回撤',
        subKpiValue: '-3.75%',
        tone: 'good',
        pdfEn: pdf('/pdfs/technical/3strat_backtest_report.pdf'),
        pdfZh: pdf('/pdfs/technical/3strat_backtest_report_ZH.pdf'),
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
        id: 'btc-lsr',
        nameZh: 'BTC 多空持仓比',
        nameEn: 'BTC Long/Short Ratio',
        description: '近 3 年累计 +125%,最差年份 −5%。',
        kpiLabel: '年化回报',
        kpiValue: '31%',
        subKpiLabel: '3 年累计',
        subKpiValue: '+125%',
        tone: 'good',
        pdfEn: pdf('/pdfs/onchain/put_call_ratio_EN.pdf'),
        pdfZh: pdf('/pdfs/onchain/put_call_ratio_ZH.pdf'),
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
        description: '系统化卖出 BTC 期权, 以 BTC 积累为目标。最大回撤仅 8%。',
        kpiLabel: '5 年累计 (BTC)',
        kpiValue: '+338%',
        subKpiLabel: 'USD 含币价',
        subKpiValue: '+433%',
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
        id: 'model-1',
        nameZh: 'Model 1',
        nameEn: 'Model 1',
        description:
          'AI 深度学习驱动的 BTC 波段交易系统。持续学习技术分析视频、交易所实时数据、图表形态及历史交易记录,自动生成并管理交易计划。系统记录每笔交易决策,复盘得失并持续优化——随着交易经验的积累不断进化。(更新: 2026-07-24)',
        kpiLabel: '累计盈亏 (模拟)',
        kpiValue: '+$2,524',
        subKpiLabel: '交易记录',
        subKpiValue: '10 笔',
        tone: 'good',
        pdfZh: pdf('/dl/model_1.html'),
        pdfZhLabel: '历史交易+交易计划',
        pdfZhIcon: '📊',
      },
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
