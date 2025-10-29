# Demo Data Dictionary

**Purpose**: Real Carozzi data for ProcureGenius demo (2015-2023)

## Directory Structure

```
demo/
├── contracts/          # Procurement contracts and tenders
│   └── licitacion_ia_20250927.pdf  # Sample AI procurement tender
└── financials/         # Annual financial statements (EEFF)
    ├── carozzi_eeff_2015.pdf
    ├── carozzi_eeff_2016.pdf
    ├── carozzi_eeff_2017.pdf
    ├── carozzi_eeff_2018.pdf
    ├── carozzi_eeff_2019.pdf
    ├── carozzi_eeff_2020.pdf
    ├── carozzi_eeff_2021.pdf
    ├── carozzi_eeff_2022.pdf
    └── carozzi_eeff_2023.pdf
```

## Data Sources

### 1. Financial Statements (2015-2023)
**Source**: Carozzi consolidated annual reports
**Format**: PDF (scanned documents)
**Content**:
- Balance sheets
- Income statements
- Cash flow statements
- Notes to financial statements
- Key metrics: Revenue, COGS, Gross Margin, Operating Margin

**Extracted Metrics** (for predictive model):
- Total Revenue (MMUSD)
- Cost of Goods Sold (COGS)
- Gross Margin %
- Operating Income
- Net Income
- Total Assets
- Working Capital

**Key Observations**:
- 2015-2019: Stable growth period
- 2020-2021: COVID-19 impact (supply chain disruptions)
- 2022-2023: Commodity price volatility (wheat, cocoa, oils)

### 2. Procurement Contracts
**Source**: Chilean public procurement portal (mercadopublico.cl)
**Format**: PDF
**Content**:
- Contract terms and conditions
- Pricing structures
- Delivery schedules
- Performance requirements
- Compliance clauses

**Sample Contract**: `licitacion_ia_20250927.pdf`
- Type: Technology services (AI/ML platform)
- Value: ~$50,000 USD
- Duration: 12 months
- Terms: Fixed price, phased delivery
- Use case: Contract parsing and analysis testing

## Data Usage

### For Predictive Intelligence
**Historical Analysis**:
1. Extract annual metrics from EEFF PDFs (2015-2023)
2. Identify external events (commodity spikes, currency devaluation)
3. Calculate correlations (cocoa price → gross margin)
4. Build predictive model (watsonx.ai + Granite 4.0)
5. Backtest validation (train: 2015-2021, test: 2022-2023)

**Target Predictions**:
- Margin impact from commodity price changes
- Supplier concentration risk scoring
- Optimal contract timing recommendations

### For Agent Demonstrations
**Contract Analysis Agent**:
- Input: `licitacion_ia_20250927.pdf`
- Output: Extracted terms, risks, recommendations
- Time: <15 seconds

**Compliance Guardian Agent**:
- Validate contract against Chilean procurement law
- Flag missing clauses (force majeure, SLA penalties)
- Suggest improvements

## Data Quality Notes

**Financial Statements**:
- ✅ Complete coverage (9 years, no gaps)
- ✅ Audited by external firms (PwC, Deloitte)
- ⚠️ Scanned PDFs require OCR (not native digital)
- ⚠️ Some tables may have extraction errors (manual verification needed)

**Contracts**:
- ✅ Real-world complexity (legal jargon, multi-party clauses)
- ✅ Representative of B2B procurement contracts
- ⚠️ Single sample (need more for statistical validation)
- ⚠️ Public sector focus (private sector terms may differ)

## External Data Requirements

**Not Included in This Directory** (to be fetched during implementation):

1. **Commodity Prices** (FRED API)
   - Cocoa (PCOCOUSDM)
   - Wheat (PWHEAMTUSDM)
   - Crude Oil (POILBREUSDM)
   - Frequency: Monthly (2015-2023)

2. **Currency Exchange Rates** (FRED API)
   - USD/CLP (Chilean Peso)
   - Frequency: Daily (aggregated to monthly)

3. **Economic Events Timeline** (Manual compilation)
   - 2015: Chilean peso devaluation (-15%)
   - 2018: Wheat price spike (+20%)
   - 2020: COVID-19 supply disruptions
   - 2022-2023: Cocoa price surge (+50%)

## Privacy & Compliance

**Public Data**: All financial statements and contracts are publicly available documents.
**No PII**: No personally identifiable information included.
**Usage**: Educational/hackathon purposes (non-commercial demo).
**Attribution**: Carozzi S.A. financial reports (https://www.carozzi.cl)

## Next Steps

**Phase 1 (George - Research)**:
- [ ] Extract key metrics from all 9 EEFF PDFs
- [ ] Compile economic events timeline
- [ ] Fetch commodity price data (FRED API)
- [ ] Calculate historical correlations

**Phase 2 (Valtteri - Implementation)**:
- [ ] Create ETL pipeline (PDF → structured data)
- [ ] Build predictive model (watsonx.ai)
- [ ] Integrate with agent workflows
- [ ] Prepare demo dataset (pre-processed)

**Phase 3 (Adrian - Verification)**:
- [ ] Validate data accuracy (spot-check 10% of extractions)
- [ ] Test predictive model (backtesting metrics)
- [ ] Verify demo reliability (5+ successful runs)

---

**Last Updated**: 2025-10-29
**Data Owner**: George (Research Agent)
**Version**: 1.0
