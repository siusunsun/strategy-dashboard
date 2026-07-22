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
        description: '前推验证组合：ATA 40% + 杯柄形态 35% + 均值回归 25%。30 币种杯柄 + 10 币种均值回归 + 6 个 ATA 子策略，策略间相关性 < 0.08。已部署 Hyperliquid，4 倍杠杆。',
        kpiLabel: 'OOS 夏普',
        kpiValue: '1.56',
        subKpiLabel: 'OOS 最大回撤',
        subKpiValue: '3.75%',
        tone: 'good',
        pdfEn: pdf('/pdfs/technical/3strat_backtest_report.pdf'),
        pdfZh: pdf('/pdfs/technical/3strat_backtest_report.pdf'),
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
        id: 'model-1',
        nameZh: 'Model 1',
        nameEn: 'Model 1',
        description:
          '以 Claude AI 为实时分析师的 BTC 波段交易系统。多源融合（市场分析视频、链上清算热力图、多空持仓、宏观日历）动态生成候选计划，从纯技术回测演化至 AI 辅助识别流动性陷阱与双向 fork 布局，目前以 1 BTC 标准仓位在模拟盘实时验证策略边际。',
        kpiLabel: '运行状态',
        kpiValue: '模拟盘运行中',
        subKpiLabel: '候选计划',
        subKpiValue: '6 条',
        tone: 'neutral',
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
