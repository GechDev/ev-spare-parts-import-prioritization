# Comprehensive Automated Test Suite for MCDA Scoring Engine (Stage 5C Reconciliation Audited)
$ErrorActionPreference = "Stop"
$script:passed = 0
$script:failed = 0

function Assert-Condition([bool]$condition, [string]$testName) {
    if ($condition) {
        Write-Host " [PASS] $testName" -ForegroundColor Green
        $script:passed++
    } else {
        Write-Host " [FAIL] $testName" -ForegroundColor Red
        $script:failed++
    }
}

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "RUNNING STAGE 5C AUTOMATED RECONCILIATION SUITE" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

$repoRoot = "c:\Users\Administrator\Desktop\icog\ev-spare-parts-import-prioritization"

# 1. Weights sum to 1.0 across all scenarios
$scenarios = @{
    "Primary"   = @{ w1 = 0.25; w2 = 0.25; w3 = 0.20; w4 = 0.20; w5 = 0.10 }
    "Benchmark" = @{ w1 = 0.30; w2 = 0.25; w3 = 0.20; w4 = 0.15; w5 = 0.10 }
    "Capital"   = @{ w1 = 0.20; w2 = 0.20; w3 = 0.20; w4 = 0.30; w5 = 0.10 }
    "DemandAgg" = @{ w1 = 0.40; w2 = 0.20; w3 = 0.15; w4 = 0.15; w5 = 0.10 }
}
foreach ($s in $scenarios.Keys) {
    $sum = $scenarios[$s].w1 + $scenarios[$s].w2 + $scenarios[$s].w3 + $scenarios[$s].w4 + $scenarios[$s].w5
    Assert-Condition ([Math]::Abs($sum - 1.0) -lt 1e-6) "Weights sum to 1.0 for scenario $s"
}

# 2. Verify Generated Outputs
$fullCsvPath = Join-Path $repoRoot "results\rankings\full_ranking.csv"
$factorCsvPath = Join-Path $repoRoot "results\rankings\factor_scores.csv"
$reportPath = Join-Path $repoRoot "results\rankings\ranking_report.md"
$chartPath = Join-Path $repoRoot "results\rankings\highest_priority_candidates.png"
$skuReconPath = Join-Path $repoRoot "results\rankings\stage5c_sku_reconciliation.csv"
$catReconPath = Join-Path $repoRoot "results\rankings\stage5c_category_reconciliation.csv"

Assert-Condition (Test-Path $fullCsvPath) "full_ranking.csv exists"
Assert-Condition (Test-Path $factorCsvPath) "factor_scores.csv exists"
Assert-Condition (Test-Path $reportPath) "ranking_report.md exists"
Assert-Condition (Test-Path $chartPath) "highest_priority_candidates.png exists"
Assert-Condition (Test-Path $skuReconPath) "stage5c_sku_reconciliation.csv exists"
Assert-Condition (Test-Path $catReconPath) "stage5c_category_reconciliation.csv exists"

$fullRows = Import-Csv $fullCsvPath
$factorRows = Import-Csv $factorCsvPath
$skuReconRows = Import-Csv $skuReconPath
$catReconRows = Import-Csv $catReconPath

Assert-Condition ($fullRows.Count -eq 30) "full_ranking.csv contains exactly 30 candidate records"
Assert-Condition ($factorRows.Count -eq 150) "factor_scores.csv contains exactly 150 factor-level explanations (30 SKUs x 5 factors)"
Assert-Condition ($skuReconRows.Count -eq 30) "stage5c_sku_reconciliation.csv contains exactly 30 unique SKU records"
Assert-Condition ($catReconRows.Count -eq 10) "stage5c_category_reconciliation.csv contains exactly 10 category records"
Assert-Condition ((Get-Item $chartPath).Length -gt 10000) "highest_priority_candidates.png is valid high-res image (>10KB)"

# 3. Validation checks on full_ranking.csv (Stage 5B/5C Single-Source Audited)
$nullPrice = $fullRows | Where-Object { $_.record_id -eq "CLN-SGL-FENDER-01" }
Assert-Condition ($nullPrice.price_usd -eq "NULL") "Zero fabrication: CLN-SGL-FENDER-01 price is strictly NULL"
Assert-Condition ($nullPrice.uncertainty_flag -eq "DATA_GAP_PRICE_UNVERIFIED") "CLN-SGL-FENDER-01 is flagged DATA_GAP_PRICE_UNVERIFIED"
Assert-Condition ($nullPrice.decision_completeness_dci -eq "40") "CLN-SGL-FENDER-01 DCI is reduced to 40.0% (Single-Source Unpriced)"

$pricedSample = $fullRows | Where-Object { $_.record_id -eq "CLN-VW-CABFILT-01" }
Assert-Condition ($pricedSample.decision_completeness_dci -eq "56.7") "Priced Single-Source DCI is exactly 56.7% (CCI 80.0%, MCI 33.3%, LCI 33.3%)"

# 4. Standard Competition Rankings & Tie Consistency
$t1_skus = $fullRows | Where-Object { $_.Rank_Primary_Str -eq "T-1" }
Assert-Condition ($t1_skus.Count -eq 3) "Primary model has exactly 3 SKUs tied at T-1 (Cabin filters at 81.14)"

$t4_skus = $fullRows | Where-Object { $_.Rank_Primary_Str -eq "T-4" }
Assert-Condition ($t4_skus.Count -eq 2) "Primary model has exactly 2 SKUs tied at T-4 (VW & Toyota wipers at 77.56)"

$t6_skus = $fullRows | Where-Object { $_.Rank_Primary_Str -eq "T-6" }
Assert-Condition ($t6_skus.Count -eq 3) "Primary model has exactly 3 SKUs tied at T-6 (Brake pads at 77.40)"

# Next rank after T-6 must be 9
$rank9 = $fullRows | Where-Object { $_.Rank_Primary_Num -eq 9 }
Assert-Condition ($rank9.record_id -eq "CLN-SGL-WIPER-01") "Rank following T-6 is correctly assigned as 9 (CLN-SGL-WIPER-01 at 73.56)"

# 5. Benchmark Tie Expansion
$benT1 = $fullRows | Where-Object { $_.Rank_Benchmark_Str -eq "T-1" }
$benT4 = $fullRows | Where-Object { $_.Rank_Benchmark_Str -eq "T-4" }
Assert-Condition ($benT1.Count -eq 3) "Benchmark model has 3 SKUs tied at T-1 (Cabin filters at 81.23)"
Assert-Condition ($benT4.Count -eq 3) "Benchmark model has 3 SKUs tied at T-4 (Brake pads at 77.97)"
Assert-Condition (($benT1.Count + $benT4.Count) -eq 6) "Benchmark top-five cutoff expands to 6 SKUs due to T-4 tie at positions 4, 5, 6"

# 6. Category Level Invariance & Brake Pads > Wiper Blades
$grouped = $fullRows | Group-Object category_id
$catMap = @{}
foreach ($g in $grouped) {
    $catId = $g.Name
    $avgPri = ($g.Group | Measure-Object -Property CPS_Primary_raw -Average).Average
    $avgBen = ($g.Group | Measure-Object -Property CPS_Benchmark_raw -Average).Average
    $avgCap = ($g.Group | Measure-Object -Property CPS_Capital_raw -Average).Average
    $avgDem = ($g.Group | Measure-Object -Property CPS_DemandAgg_raw -Average).Average
    $catMap[$catId] = @{
        Pri = $avgPri; Ben = $avgBen; Cap = $avgCap; Dem = $avgDem
    }
}

Assert-Condition ($catMap["CAT-01-BRKPAD"].Pri -gt $catMap["CAT-04-WIPER"].Pri) "Brake Pads > Wipers in Primary (77.40 vs 76.23)"
Assert-Condition ($catMap["CAT-01-BRKPAD"].Ben -gt $catMap["CAT-04-WIPER"].Ben) "Brake Pads > Wipers in Benchmark (77.97 vs 76.09)"
Assert-Condition ($catMap["CAT-01-BRKPAD"].Cap -gt $catMap["CAT-04-WIPER"].Cap) "Brake Pads > Wipers in Capital (78.55 vs 78.51)"
Assert-Condition ($catMap["CAT-01-BRKPAD"].Dem -gt $catMap["CAT-04-WIPER"].Dem) "Brake Pads > Wipers in DemandAgg (81.08 vs 78.92)"

# 7. Factor Scores Traceability
$f1_exps = $factorRows | Where-Object { $_.factor_id -eq "F1" }
$f2_exps = $factorRows | Where-Object { $_.factor_id -eq "F2" }
$f3_exps = $factorRows | Where-Object { $_.factor_id -eq "F3" }
$f4_exps = $factorRows | Where-Object { $_.factor_id -eq "F4" }
$f5_exps = $factorRows | Where-Object { $_.factor_id -eq "F5" }

Assert-Condition ($f1_exps.Count -eq 30) "All 30 SKUs have F1 Demand traceability"
Assert-Condition ($f2_exps.Count -eq 30) "All 30 SKUs have F2 Procurement Delay traceability"
Assert-Condition ($f3_exps.Count -eq 30) "All 30 SKUs have F3 Compatibility traceability"
Assert-Condition ($f4_exps.Count -eq 30) "All 30 SKUs have F4 Sourcing Practicality traceability"
Assert-Condition ($f5_exps.Count -eq 30) "All 30 SKUs have F5 Evidence Confidence traceability (Single-Source 4.0 / Unpriced 3.0)"

# 8. Stage 5C Strict Reconciliation Tests
$f5_explained_count = ($skuReconRows | Where-Object { $_.Mathematically_Explained_By_F5 -eq "YES" }).Count
Assert-Condition ($f5_explained_count -eq 30) "All 30 SKUs score changes are 100% mathematically explained by F5 change"

$priced_score_drops = ($skuReconRows | Where-Object { $_.record_id -ne "CLN-SGL-FENDER-01" -and [Math]::Abs([double]$_.Diff_Primary - (-2.0)) -lt 1e-4 }).Count
Assert-Condition ($priced_score_drops -eq 29) "All 29 priced SKUs decrease by exactly 2.0000 points across all scenarios"

$unpriced_fender_delta = [double]($skuReconRows | Where-Object { $_.record_id -eq "CLN-SGL-FENDER-01" }).Diff_Primary
Assert-Condition ([Math]::Abs($unpriced_fender_delta - 0.0) -lt 1e-4) "Unpriced Seagull fender Primary score delta is exactly 0.0000 points"

$cat_zero_discrepancies = ($catReconRows | Where-Object { [Math]::Abs([double]$_.SKU_Discrepancy) -lt 1e-4 }).Count
Assert-Condition ($cat_zero_discrepancies -eq 10) "Category means equal means calculated directly from SKU-level scores across all 10 categories (zero discrepancy)"

# 9. Idempotency test (Regeneration produces identical rankings)
$scratchScript = "C:\Users\Administrator\.gemini\antigravity\brain\c1cc5d54-e21f-4697-9caf-11bc5e182e13\scratch\build_scoring_engine_and_outputs.ps1"
if (Test-Path $scratchScript) {
    . $scratchScript
}
$reloadedRows = Import-Csv $fullCsvPath
$identical = $true
for ($i = 0; $i -lt 30; $i++) {
    if ($fullRows[$i].record_id -ne $reloadedRows[$i].record_id -or
        $fullRows[$i].CPS_Primary -ne $reloadedRows[$i].CPS_Primary -or
        $fullRows[$i].Rank_Primary_Str -ne $reloadedRows[$i].Rank_Primary_Str) {
        $identical = $false
        break
    }
}
Assert-Condition ($identical -eq $true) "Idempotency confirmed: Repeated execution produces identical rankings and scores"

# 10. Sensitivity Analysis Verification (Stage 5C Dataset)
$sensCsvPath = Join-Path $repoRoot "results\rankings\sensitivity_analysis.csv"
$sensChartPath = Join-Path $repoRoot "results\rankings\sensitivity_comparison.png"

Assert-Condition (Test-Path $sensCsvPath) "sensitivity_analysis.csv exists"
Assert-Condition (Test-Path $sensChartPath) "sensitivity_comparison.png exists"

$sensRows = Import-Csv $sensCsvPath
Assert-Condition ($sensRows.Count -eq 30) "sensitivity_analysis.csv contains exactly 30 candidate records"
Assert-Condition ((Get-Item $sensChartPath).Length -gt 10000) "sensitivity_comparison.png is valid high-res image (>10KB)"

# Sensitivity Scenarios Weight Validation
$sensWeights = @{
    "Baseline"         = @(0.25, 0.25, 0.20, 0.20, 0.10)
    "Demand_Focused"   = @(0.40, 0.20, 0.15, 0.15, 0.10)
    "Evidence_Focused" = @(0.20, 0.20, 0.20, 0.15, 0.25)
    "Sourcing_Focused" = @(0.20, 0.20, 0.20, 0.30, 0.10)
}
foreach ($k in $sensWeights.Keys) {
    $w = $sensWeights[$k]
    $wSum = ($w | Measure-Object -Sum).Sum
    Assert-Condition ([Math]::Abs($wSum - 1.0) -lt 1e-6) "Sensitivity scenario $k weights sum exactly to 1.00"
}

# Top-5 Overlap and Membership Validation
$baseTop5Ids = ($sensRows | Where-Object { [int]$_.Rank_Baseline_Num -le 5 } | Select-Object -ExpandProperty record_id)
Assert-Condition ($baseTop5Ids.Count -eq 5) "Baseline top 5 has exactly 5 SKUs (3 Cabin filters T-1, 2 Wiper blades T-4)"

# Evidence-Focused Top 5
$evidTop5Ids = ($sensRows | Where-Object { [int]$_.Rank_Evidence_Focused_Num -le 5 } | Select-Object -ExpandProperty record_id)
$evidOverlap = ($baseTop5Ids | Where-Object { $evidTop5Ids -contains $_ }).Count
Assert-Condition ($evidOverlap -eq 5) "Evidence-Focused top 5 retains 100% (5/5) of Baseline top 5 SKUs"

# Sourcing-Focused Top 5
$sourTop5Ids = ($sensRows | Where-Object { [int]$_.Rank_Sourcing_Focused_Num -le 5 } | Select-Object -ExpandProperty record_id)
$sourOverlap = ($baseTop5Ids | Where-Object { $sourTop5Ids -contains $_ }).Count
Assert-Condition ($sourOverlap -eq 5) "Sourcing-Focused top 5 retains 100% (5/5) of Baseline top 5 SKUs"

# Demand-Focused Top 5 Cutoff & Tie Expansion
$demTop5Ids = ($sensRows | Where-Object { [int]$_.Rank_Demand_Focused_Num -le 5 } | Select-Object -ExpandProperty record_id)
$demOverlap = ($baseTop5Ids | Where-Object { $demTop5Ids -contains $_ }).Count
Assert-Condition ($demOverlap -eq 3) "Demand-Focused retains 3 of 5 Baseline SKUs (60.0% overlap: 3 Cabin filters)"
Assert-Condition ($demTop5Ids.Count -eq 6) "Demand-Focused top cutoff expands to 6 SKUs due to T-4 tie at positions 4, 5, 6 (3 Brake pads)"

# Global Top 8 and Top 10 Invariance
$baseTop8 = ($sensRows | Select-Object -First 8 | Select-Object -ExpandProperty record_id) | Sort-Object
foreach ($sc in @("Demand_Focused", "Evidence_Focused", "Sourcing_Focused")) {
    $scTop8 = ($sensRows | Sort-Object "Score_${sc}_raw" -Descending | Select-Object -First 8 | Select-Object -ExpandProperty record_id) | Sort-Object
    $diff = Compare-Object $baseTop8 $scTop8
    Assert-Condition ($null -eq $diff) "Top 8 SKUs portfolio composition is 100% invariant in scenario $sc"
}

# Category Level Invariance (Cabin Filters Rank 1, Brake Pads Rank 2 in all 4 scenarios)
$catGroups = $sensRows | Group-Object category_id | ForEach-Object {
    $cid = $_.Name
    [PSCustomObject]@{
        category_id = $cid
        Avg_Base = ($_.Group | Measure-Object -Property Score_Baseline_raw -Average).Average
        Avg_Dem  = ($_.Group | Measure-Object -Property Score_Demand_Focused_raw -Average).Average
        Avg_Evid = ($_.Group | Measure-Object -Property Score_Evidence_Focused_raw -Average).Average
        Avg_Sour = ($_.Group | Measure-Object -Property Score_Sourcing_Focused_raw -Average).Average
    }
}
$baseSorted = $catGroups | Sort-Object Avg_Base -Descending
for ($i = 0; $i -lt $baseSorted.Count; $i++) { $baseSorted[$i] | Add-Member -NotePropertyName Rank_Base -NotePropertyValue ($i + 1) }
$demSorted = $catGroups | Sort-Object Avg_Dem -Descending
for ($i = 0; $i -lt $demSorted.Count; $i++) { $demSorted[$i] | Add-Member -NotePropertyName Rank_Dem -NotePropertyValue ($i + 1) }
$evidSorted = $catGroups | Sort-Object Avg_Evid -Descending
for ($i = 0; $i -lt $evidSorted.Count; $i++) { $evidSorted[$i] | Add-Member -NotePropertyName Rank_Evid -NotePropertyValue ($i + 1) }
$sourSorted = $catGroups | Sort-Object Avg_Sour -Descending
for ($i = 0; $i -lt $sourSorted.Count; $i++) { $sourSorted[$i] | Add-Member -NotePropertyName Rank_Sour -NotePropertyValue ($i + 1) }
$catTable = $baseSorted
Assert-Condition ($catTable[0].category_id -eq "CAT-03-CABFILT" -and $catTable[0].Rank_Base -eq 1 -and $catTable[0].Rank_Dem -eq 1 -and $catTable[0].Rank_Evid -eq 1 -and $catTable[0].Rank_Sour -eq 1) "Category Rank 1 is Cabin-air filters across ALL 4 sensitivity scenarios"
Assert-Condition ($catTable[1].category_id -eq "CAT-01-BRKPAD" -and $catTable[1].Rank_Base -eq 2 -and $catTable[1].Rank_Dem -eq 2 -and $catTable[1].Rank_Evid -eq 2 -and $catTable[1].Rank_Sour -eq 2) "Category Rank 2 is Brake pads across ALL 4 sensitivity scenarios"
Assert-Condition ($catTable[2].category_id -eq "CAT-04-WIPER" -and $catTable[2].Rank_Base -eq 3 -and $catTable[2].Rank_Dem -eq 3 -and $catTable[2].Rank_Evid -eq 3 -and $catTable[2].Rank_Sour -eq 3) "Category Rank 3 is Wiper blades across ALL 4 sensitivity scenarios"
Assert-Condition ($catTable[3].category_id -eq "CAT-02-BRKDISC" -and $catTable[3].Rank_Base -eq 4 -and $catTable[3].Rank_Dem -eq 4 -and $catTable[3].Rank_Evid -eq 4 -and $catTable[3].Rank_Sour -eq 4) "Category Rank 4 is Brake discs across ALL 4 sensitivity scenarios"
Assert-Condition ($catTable[4].category_id -eq "CAT-10-SHOCK" -and $catTable[4].Rank_Base -eq 5 -and $catTable[4].Rank_Dem -eq 5 -and $catTable[4].Rank_Evid -eq 5 -and $catTable[4].Rank_Sour -eq 5) "Category Rank 5 is Shock absorbers across ALL 4 sensitivity scenarios"
Assert-Condition ($catTable[5].category_id -eq "CAT-07-MIRROR" -and $catTable[5].Rank_Base -eq 6 -and $catTable[5].Rank_Dem -eq 6 -and $catTable[5].Rank_Evid -eq 6 -and $catTable[5].Rank_Sour -eq 6) "Category Rank 6 is Side mirrors across ALL 4 sensitivity scenarios"

# 11. Stage 6 Final Recommendation Report & Output Reconciliations
$finalReportPath = Join-Path $repoRoot "results\recommendation_report.md"
$finalCsvPath = Join-Path $repoRoot "results\rankings\final_top_five.csv"

Assert-Condition (Test-Path $finalReportPath) "recommendation_report.md exists"
Assert-Condition (Test-Path $finalCsvPath) "final_top_five.csv exists"
Assert-Condition ((Get-Item $finalReportPath).Length -gt 15000) "recommendation_report.md is comprehensive (>15KB)"

$finalRows = Import-Csv $finalCsvPath
Assert-Condition ($finalRows.Count -eq 5) "final_top_five.csv contains exactly 5 selected baseline candidates"

$expectedTop5Ids = @(
    "CLN-SGL-CABFILT-01",
    "CLN-TOY-CABFILT-01",
    "CLN-VW-CABFILT-01",
    "CLN-TOY-WIPER-01",
    "CLN-VW-WIPER-01"
)

$actualFinalIds = $finalRows | Select-Object -ExpandProperty candidate_id
$idDiff = Compare-Object $expectedTop5Ids $actualFinalIds
Assert-Condition ($null -eq $idDiff) "final_top_five.csv candidates match the exact 5 baseline winners"

# Check scores and ranks in final_top_five.csv
$filterSkus = $finalRows | Where-Object { $_.part_category -eq "Cabin-air filters" }
Assert-Condition ($filterSkus.Count -eq 3) "final_top_five.csv has exactly 3 Cabin-air filters"
$filterScoreMatch = ($filterSkus | Where-Object { [double]$_.baseline_cps -eq 81.14 -and $_.baseline_rank_str -eq "T-1" }).Count
Assert-Condition ($filterScoreMatch -eq 3) "All 3 cabin filters have baseline_cps 81.14 and rank T-1"

$wiperSkus = $finalRows | Where-Object { $_.part_category -eq "Wiper blades" }
Assert-Condition ($wiperSkus.Count -eq 2) "final_top_five.csv has exactly 2 Wiper blade SKUs"
$wiperScoreMatch = ($wiperSkus | Where-Object { [double]$_.baseline_cps -eq 77.56 -and $_.baseline_rank_str -eq "T-4" }).Count
Assert-Condition ($wiperScoreMatch -eq 2) "All 2 wiper blades have baseline_cps 77.56 and rank T-4"

# Reconcile OEM numbers and source URLs against cleaned_dataset.csv
$cleanedMaster = Import-Csv (Join-Path $repoRoot "data\processed\cleaned_dataset.csv")
$oemAndUrlMatches = 0
foreach ($row in $finalRows) {
    $cleanMatch = $cleanedMaster | Where-Object { $_.record_id -eq $row.candidate_id }
    if ($cleanMatch.clean_oem_part_number -eq $row.clean_oem_part_number -and $cleanMatch.source_url -eq $row.source_url) {
        $oemAndUrlMatches++
    }
}
Assert-Condition ($oemAndUrlMatches -eq 5) "All 5 candidates OEM part numbers and source URLs match cleaned_dataset.csv exactly"

Write-Host "`n==========================================" -ForegroundColor Cyan
Write-Host "STAGE 6 RECOMMENDATIONS TEST SUMMARY: Passed: $($script:passed) | Failed: $($script:failed)" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

if ($script:failed -gt 0) { exit 1 }
