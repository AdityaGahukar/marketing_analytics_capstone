
# data_dict = [

#     # ─────────────────────────────────────
#     #  TABLE 1 — DIM_CAMPAIGN
#     # ─────────────────────────────────────
#     {
#         "table": "DIM_CAMPAIGN",
#         "schema": "gold",
#         "description": "Master dimension for all marketing campaigns. One row per campaign.",
#         "grain": "One row per CAMPAIGN_ID",
#         "columns": [
#             {"column": "CAMPAIGN_ID",          "type": "VARCHAR(50)",   "pk": True,  "fk": None,                              "nullable": False, "description": "Primary key. Unique campaign ID from ad platform."},
#             {"column": "CAMPAIGN_NAME",        "type": "VARCHAR(255)",  "pk": False, "fk": None,                              "nullable": False, "description": "Human-readable campaign name as set in the ad platform."},
#             {"column": "PLATFORM",             "type": "VARCHAR(50)",   "pk": False, "fk": None,                              "nullable": False, "description": "Ad platform. Allowed values: 'GOOGLE', 'META', 'LINKEDIN', 'TWITTER', 'TIKTOK', 'EMAIL', 'ORGANIC'"},
#             {"column": "CAMPAIGN_TYPE",        "type": "VARCHAR(50)",   "pk": False, "fk": None,                              "nullable": True,  "description": "Campaign type. Allowed values: 'SEARCH', 'DISPLAY', 'VIDEO', 'SHOPPING', 'SOCIAL', 'EMAIL', 'RETARGETING'"},
#             {"column": "CAMPAIGN_OBJECTIVE",   "type": "VARCHAR(100)",  "pk": False, "fk": None,                              "nullable": True,  "description": "Campaign goal. Allowed values: 'BRAND_AWARENESS', 'LEAD_GENERATION', 'CONVERSIONS', 'TRAFFIC', 'ENGAGEMENT', 'RETENTION'"},
#             {"column": "CAMPAIGN_STATUS",      "type": "VARCHAR(20)",   "pk": False, "fk": None,                              "nullable": False, "description": "Status. Allowed values: 'ACTIVE', 'PAUSED', 'ENDED', 'DRAFT'"},
#             {"column": "START_DATE",           "type": "DATE",          "pk": False, "fk": None,                              "nullable": False, "description": "Campaign start date (YYYY-MM-DD)."},
#             {"column": "END_DATE",             "type": "DATE",          "pk": False, "fk": None,                              "nullable": True,  "description": "Campaign end date. NULL if campaign is still ongoing."},
#             {"column": "TARGET_AUDIENCE",      "type": "VARCHAR(255)",  "pk": False, "fk": None,                              "nullable": True,  "description": "Free-text description of the target audience segment."},
#             {"column": "TARGET_GEOGRAPHY",     "type": "VARCHAR(255)",  "pk": False, "fk": None,                              "nullable": True,  "description": "Targeted geographic regions, comma-separated."},
#             {"column": "BUDGET_TYPE",          "type": "VARCHAR(20)",   "pk": False, "fk": None,                              "nullable": True,  "description": "Budget cadence. Allowed values: 'DAILY', 'LIFETIME', 'MONTHLY'"},
#             {"column": "TOTAL_BUDGET_USD",     "type": "NUMBER(18,2)",  "pk": False, "fk": None,                              "nullable": True,  "description": "Total allocated budget in USD."},
#             {"column": "CREATED_AT",           "type": "TIMESTAMP_NTZ", "pk": False, "fk": None,                              "nullable": False, "description": "Row creation timestamp."},
#             {"column": "UPDATED_AT",           "type": "TIMESTAMP_NTZ", "pk": False, "fk": None,                              "nullable": False, "description": "Row last updated timestamp."},
#         ],
#         "relationships": [
#             "CAMPAIGN_ID → FACT_AD_PERFORMANCE.CAMPAIGN_ID",
#             "CAMPAIGN_ID → FACT_SPEND.CAMPAIGN_ID",
#             "CAMPAIGN_ID → FACT_CONVERSIONS.CAMPAIGN_ID",
#         ]
#     },

#     # ─────────────────────────────────────
#     #  TABLE 2 — DIM_AD_GROUP
#     # ─────────────────────────────────────
#     {
#         "table": "DIM_AD_GROUP",
#         "schema": "gold",
#         "description": "Ad groups or ad sets within a campaign. Child of DIM_CAMPAIGN.",
#         "grain": "One row per AD_GROUP_ID",
#         "columns": [
#             {"column": "AD_GROUP_ID",          "type": "VARCHAR(50)",   "pk": True,  "fk": None,                              "nullable": False, "description": "Primary key. Unique ad group / ad set ID."},
#             {"column": "AD_GROUP_NAME",        "type": "VARCHAR(255)",  "pk": False, "fk": None,                              "nullable": False, "description": "Name of the ad group or ad set."},
#             {"column": "CAMPAIGN_ID",          "type": "VARCHAR(50)",   "pk": False, "fk": "DIM_CAMPAIGN.CAMPAIGN_ID",        "nullable": False, "description": "Foreign key to DIM_CAMPAIGN."},
#             {"column": "BID_STRATEGY",         "type": "VARCHAR(100)",  "pk": False, "fk": None,                              "nullable": True,  "description": "Bidding strategy. Allowed values: 'CPC', 'CPM', 'CPA', 'ROAS_TARGET', 'MANUAL_CPC', 'ENHANCED_CPC', 'TARGET_IMPRESSION_SHARE'"},
#             {"column": "BID_AMOUNT_USD",       "type": "NUMBER(18,4)",  "pk": False, "fk": None,                              "nullable": True,  "description": "Manual bid amount in USD. NULL when automated bidding is used."},
#             {"column": "AD_GROUP_STATUS",      "type": "VARCHAR(20)",   "pk": False, "fk": None,                              "nullable": False, "description": "Status. Allowed values: 'ACTIVE', 'PAUSED', 'REMOVED'"},
#             {"column": "TARGETING_TYPE",       "type": "VARCHAR(50)",   "pk": False, "fk": None,                              "nullable": True,  "description": "Audience targeting method. Allowed values: 'KEYWORD', 'INTEREST', 'LOOKALIKE', 'REMARKETING', 'DEMOGRAPHIC', 'CONTEXTUAL'"},
#             {"column": "CREATED_AT",           "type": "TIMESTAMP_NTZ", "pk": False, "fk": None,                              "nullable": False, "description": "Row creation timestamp."},
#             {"column": "UPDATED_AT",           "type": "TIMESTAMP_NTZ", "pk": False, "fk": None,                              "nullable": False, "description": "Row last updated timestamp."},
#         ],
#         "relationships": [
#             "AD_GROUP_ID → FACT_AD_PERFORMANCE.AD_GROUP_ID",
#             "CAMPAIGN_ID → DIM_CAMPAIGN.CAMPAIGN_ID",
#         ]
#     },

#     # ─────────────────────────────────────
#     #  TABLE 3 — DIM_AD_CREATIVE
#     # ─────────────────────────────────────
#     {
#         "table": "DIM_AD_CREATIVE",
#         "schema": "gold",
#         "description": "Individual ad creatives — the actual ads shown to users.",
#         "grain": "One row per AD_CREATIVE_ID",
#         "columns": [
#             {"column": "AD_CREATIVE_ID",       "type": "VARCHAR(50)",   "pk": True,  "fk": None,                              "nullable": False, "description": "Primary key. Unique ad creative ID."},
#             {"column": "AD_GROUP_ID",          "type": "VARCHAR(50)",   "pk": False, "fk": "DIM_AD_GROUP.AD_GROUP_ID",        "nullable": False, "description": "Foreign key to DIM_AD_GROUP."},
#             {"column": "CAMPAIGN_ID",          "type": "VARCHAR(50)",   "pk": False, "fk": "DIM_CAMPAIGN.CAMPAIGN_ID",        "nullable": False, "description": "Denormalized FK to DIM_CAMPAIGN for query convenience."},
#             {"column": "AD_NAME",              "type": "VARCHAR(255)",  "pk": False, "fk": None,                              "nullable": False, "description": "Label or name of the ad creative."},
#             {"column": "AD_FORMAT",            "type": "VARCHAR(50)",   "pk": False, "fk": None,                              "nullable": False, "description": "Creative format. Allowed values: 'IMAGE', 'VIDEO', 'CAROUSEL', 'TEXT', 'RESPONSIVE', 'STORY', 'REEL', 'HTML5'"},
#             {"column": "HEADLINE",             "type": "VARCHAR(500)",  "pk": False, "fk": None,                              "nullable": True,  "description": "Primary headline text of the ad."},
#             {"column": "DESCRIPTION",          "type": "VARCHAR(1000)", "pk": False, "fk": None,                              "nullable": True,  "description": "Body/description text of the ad."},
#             {"column": "CALL_TO_ACTION",       "type": "VARCHAR(100)",  "pk": False, "fk": None,                              "nullable": True,  "description": "CTA button text. Examples: 'LEARN_MORE', 'SIGN_UP', 'BUY_NOW', 'GET_QUOTE', 'DOWNLOAD'"},
#             {"column": "DESTINATION_URL",      "type": "VARCHAR(2000)", "pk": False, "fk": None,                              "nullable": True,  "description": "Final landing page URL without tracking parameters."},
#             {"column": "CREATIVE_STATUS",      "type": "VARCHAR(20)",   "pk": False, "fk": None,                              "nullable": False, "description": "Status. Allowed values: 'ACTIVE', 'PAUSED', 'DISAPPROVED', 'ARCHIVED'"},
#             {"column": "CREATED_AT",           "type": "TIMESTAMP_NTZ", "pk": False, "fk": None,                              "nullable": False, "description": "Row creation timestamp."},
#             {"column": "UPDATED_AT",           "type": "TIMESTAMP_NTZ", "pk": False, "fk": None,                              "nullable": False, "description": "Row last updated timestamp."},
#         ],
#         "relationships": [
#             "AD_CREATIVE_ID → FACT_AD_PERFORMANCE.AD_CREATIVE_ID",
#             "AD_GROUP_ID → DIM_AD_GROUP.AD_GROUP_ID",
#         ]
#     },

#     # ─────────────────────────────────────
#     #  TABLE 4 — DIM_DATE
#     # ─────────────────────────────────────
#     {
#         "table": "DIM_DATE",
#         "schema": "gold",
#         "description": "Calendar date dimension. One row per day. Use for all date filtering and grouping.",
#         "grain": "One row per DATE_KEY (calendar day)",
#         "columns": [
#             {"column": "DATE_KEY",             "type": "DATE",          "pk": True,  "fk": None,  "nullable": False, "description": "Primary key. Calendar date in YYYY-MM-DD format."},
#             {"column": "DAY_OF_WEEK",          "type": "VARCHAR(10)",   "pk": False, "fk": None,  "nullable": False, "description": "Full day name. Values: 'Monday' through 'Sunday'"},
#             {"column": "DAY_OF_WEEK_NUM",      "type": "NUMBER(1)",     "pk": False, "fk": None,  "nullable": False, "description": "Day number. 1=Sunday ... 7=Saturday (Snowflake DAYOFWEEK convention)."},
#             {"column": "DAY_OF_MONTH",         "type": "NUMBER(2)",     "pk": False, "fk": None,  "nullable": False, "description": "Day of month (1–31)."},
#             {"column": "WEEK_OF_YEAR",         "type": "NUMBER(2)",     "pk": False, "fk": None,  "nullable": False, "description": "ISO week number (1–53)."},
#             {"column": "MONTH_NUM",            "type": "NUMBER(2)",     "pk": False, "fk": None,  "nullable": False, "description": "Month number (1–12)."},
#             {"column": "MONTH_NAME",           "type": "VARCHAR(10)",   "pk": False, "fk": None,  "nullable": False, "description": "Full month name. Values: 'January' through 'December'"},
#             {"column": "MONTH_SHORT",          "type": "VARCHAR(3)",    "pk": False, "fk": None,  "nullable": False, "description": "3-letter month abbreviation: 'Jan', 'Feb', ... 'Dec'"},
#             {"column": "QUARTER",              "type": "NUMBER(1)",     "pk": False, "fk": None,  "nullable": False, "description": "Quarter number (1–4)."},
#             {"column": "YEAR",                 "type": "NUMBER(4)",     "pk": False, "fk": None,  "nullable": False, "description": "4-digit year."},
#             {"column": "YEAR_MONTH",           "type": "VARCHAR(7)",    "pk": False, "fk": None,  "nullable": False, "description": "Month label formatted as 'YYYY-MM'. Use this for month-wise display in results."},
#             {"column": "IS_WEEKEND",           "type": "BOOLEAN",       "pk": False, "fk": None,  "nullable": False, "description": "TRUE if Saturday or Sunday."},
#             {"column": "IS_HOLIDAY",           "type": "BOOLEAN",       "pk": False, "fk": None,  "nullable": False, "description": "TRUE if a public holiday (India + US calendar)."},
#         ],
#         "relationships": [
#             "DATE_KEY → FACT_AD_PERFORMANCE.EVENT_DATE",
#             "DATE_KEY → FACT_SPEND.SPEND_DATE",
#             "DATE_KEY → FACT_CONVERSIONS.CONVERSION_DATE",
#         ]
#     },

#     # ─────────────────────────────────────
#     #  TABLE 5 — FACT_AD_PERFORMANCE
#     # ─────────────────────────────────────
#     {
#         "table": "FACT_AD_PERFORMANCE",
#         "schema": "gold",
#         "description": "Core daily performance fact table. One row per (date, campaign, ad_group, ad_creative, platform). Primary table for CTR, impressions, clicks queries.",
#         "grain": "Daily — one row per (EVENT_DATE, CAMPAIGN_ID, AD_GROUP_ID, AD_CREATIVE_ID, PLATFORM)",
#         "columns": [
#             {"column": "PERFORMANCE_ID",       "type": "VARCHAR(100)",  "pk": True,  "fk": None,                                    "nullable": False, "description": "Surrogate PK. Hash of grain columns."},
#             {"column": "EVENT_DATE",           "type": "DATE",          "pk": False, "fk": "DIM_DATE.DATE_KEY",                     "nullable": False, "description": "Date of the performance data. FK to DIM_DATE.DATE_KEY."},
#             {"column": "CAMPAIGN_ID",          "type": "VARCHAR(50)",   "pk": False, "fk": "DIM_CAMPAIGN.CAMPAIGN_ID",              "nullable": False, "description": "FK to DIM_CAMPAIGN."},
#             {"column": "AD_GROUP_ID",          "type": "VARCHAR(50)",   "pk": False, "fk": "DIM_AD_GROUP.AD_GROUP_ID",              "nullable": False, "description": "FK to DIM_AD_GROUP."},
#             {"column": "AD_CREATIVE_ID",       "type": "VARCHAR(50)",   "pk": False, "fk": "DIM_AD_CREATIVE.AD_CREATIVE_ID",        "nullable": True,  "description": "FK to DIM_AD_CREATIVE. NULL if not tracked at creative level."},
#             {"column": "PLATFORM",             "type": "VARCHAR(50)",   "pk": False, "fk": None,                                    "nullable": False, "description": "Denormalized platform name. Allowed values: 'GOOGLE', 'META', 'LINKEDIN', 'TWITTER', 'TIKTOK', 'EMAIL', 'ORGANIC'"},
#             {"column": "IMPRESSIONS",          "type": "NUMBER(18,0)",  "pk": False, "fk": None,                                    "nullable": False, "description": "Total times the ad was shown. One user can generate multiple impressions."},
#             {"column": "CLICKS",               "type": "NUMBER(18,0)",  "pk": False, "fk": None,                                    "nullable": False, "description": "Total clicks on the ad."},
#             {"column": "VIDEO_VIEWS",          "type": "NUMBER(18,0)",  "pk": False, "fk": None,                                    "nullable": True,  "description": "Total video views. NULL for non-video ad formats. Use COALESCE(VIDEO_VIEWS, 0) when aggregating."},
#             {"column": "VIDEO_VIEW_25_PCT",    "type": "NUMBER(18,0)",  "pk": False, "fk": None,                                    "nullable": True,  "description": "Users who watched at least 25% of the video. NULL for non-video."},
#             {"column": "VIDEO_VIEW_50_PCT",    "type": "NUMBER(18,0)",  "pk": False, "fk": None,                                    "nullable": True,  "description": "Users who watched at least 50% of the video. NULL for non-video."},
#             {"column": "VIDEO_VIEW_75_PCT",    "type": "NUMBER(18,0)",  "pk": False, "fk": None,                                    "nullable": True,  "description": "Users who watched at least 75% of the video. NULL for non-video."},
#             {"column": "VIDEO_VIEW_100_PCT",   "type": "NUMBER(18,0)",  "pk": False, "fk": None,                                    "nullable": True,  "description": "Users who watched the full video. NULL for non-video."},
#             {"column": "REACH",                "type": "NUMBER(18,0)",  "pk": False, "fk": None,                                    "nullable": True,  "description": "Unique users who saw the ad. REACH != IMPRESSIONS. One user can have many impressions but only 1 reach."},
#             {"column": "FREQUENCY",            "type": "NUMBER(10,4)",  "pk": False, "fk": None,                                    "nullable": True,  "description": "Average times a unique user saw the ad. = IMPRESSIONS / REACH"},
#             {"column": "ENGAGEMENTS",          "type": "NUMBER(18,0)",  "pk": False, "fk": None,                                    "nullable": True,  "description": "Total social engagements: likes, shares, comments, saves combined."},
#             {"column": "LINK_CLICKS",          "type": "NUMBER(18,0)",  "pk": False, "fk": None,                                    "nullable": True,  "description": "Clicks specifically on the CTA link. Subset of CLICKS. Use for landing page traffic analysis."},
#             {"column": "POST_CLICK_SESSIONS",  "type": "NUMBER(18,0)",  "pk": False, "fk": None,                                    "nullable": True,  "description": "Website sessions attributed to an ad click (sourced from analytics platform)."},
#             {"column": "CREATED_AT",           "type": "TIMESTAMP_NTZ", "pk": False, "fk": None,                                    "nullable": False, "description": "Row load timestamp."},
#         ],
#         "calculated_metrics": [
#             {"metric": "CTR",             "formula": "SUM(CLICKS) / NULLIF(SUM(IMPRESSIONS), 0)",                                   "description": "Click-Through Rate. NOT a stored column — always calculate."},
#             {"metric": "CTR_PERCENT",     "formula": "ROUND(SUM(CLICKS) / NULLIF(SUM(IMPRESSIONS), 0) * 100, 4)",                   "description": "CTR expressed as percentage."},
#             {"metric": "VTR",             "formula": "SUM(VIDEO_VIEWS) / NULLIF(SUM(IMPRESSIONS), 0)",                              "description": "Video View-Through Rate. Only meaningful for VIDEO format."},
#             {"metric": "ENGAGEMENT_RATE", "formula": "SUM(ENGAGEMENTS) / NULLIF(SUM(IMPRESSIONS), 0)",                              "description": "Engagement Rate. NOT a stored column — always calculate."},
#             {"metric": "LINK_CTR",        "formula": "SUM(LINK_CLICKS) / NULLIF(SUM(IMPRESSIONS), 0)",                              "description": "Link Click-Through Rate. NOT a stored column — always calculate."},
#         ],
#         "relationships": [
#             "EVENT_DATE → DIM_DATE.DATE_KEY",
#             "CAMPAIGN_ID → DIM_CAMPAIGN.CAMPAIGN_ID",
#             "AD_GROUP_ID → DIM_AD_GROUP.AD_GROUP_ID",
#             "AD_CREATIVE_ID → DIM_AD_CREATIVE.AD_CREATIVE_ID",
#         ]
#     },

#     # ─────────────────────────────────────
#     #  TABLE 6 — FACT_SPEND
#     # ─────────────────────────────────────
#     {
#         "table": "FACT_SPEND",
#         "schema": "gold",
#         "description": "Daily ad spend fact table. One row per (date, campaign, ad_group, platform). Use for budget, cost, CPM, CPC analysis.",
#         "grain": "Daily — one row per (SPEND_DATE, CAMPAIGN_ID, AD_GROUP_ID, PLATFORM)",
#         "columns": [
#             {"column": "SPEND_ID",             "type": "VARCHAR(100)",  "pk": True,  "fk": None,                              "nullable": False, "description": "Surrogate PK."},
#             {"column": "SPEND_DATE",           "type": "DATE",          "pk": False, "fk": "DIM_DATE.DATE_KEY",               "nullable": False, "description": "Date of the spend. FK to DIM_DATE.DATE_KEY."},
#             {"column": "CAMPAIGN_ID",          "type": "VARCHAR(50)",   "pk": False, "fk": "DIM_CAMPAIGN.CAMPAIGN_ID",        "nullable": False, "description": "FK to DIM_CAMPAIGN."},
#             {"column": "AD_GROUP_ID",          "type": "VARCHAR(50)",   "pk": False, "fk": "DIM_AD_GROUP.AD_GROUP_ID",        "nullable": True,  "description": "FK to DIM_AD_GROUP. NULL if spend is only tracked at campaign level."},
#             {"column": "PLATFORM",             "type": "VARCHAR(50)",   "pk": False, "fk": None,                              "nullable": False, "description": "Denormalized platform name."},
#             {"column": "AMOUNT_SPENT_USD",     "type": "NUMBER(18,4)",  "pk": False, "fk": None,                              "nullable": False, "description": "Actual amount spent on this date in USD. Already converted from source currency."},
#             {"column": "IMPRESSIONS",          "type": "NUMBER(18,0)",  "pk": False, "fk": None,                              "nullable": False, "description": "Impressions on this date. Used for CPM calculation."},
#             {"column": "CLICKS",               "type": "NUMBER(18,0)",  "pk": False, "fk": None,                              "nullable": False, "description": "Clicks on this date. Used for CPC calculation."},
#             {"column": "CURRENCY_CODE",        "type": "VARCHAR(3)",    "pk": False, "fk": None,                              "nullable": False, "description": "Original source currency code e.g. 'USD', 'INR'. Conversion already applied in AMOUNT_SPENT_USD."},
#             {"column": "CREATED_AT",           "type": "TIMESTAMP_NTZ", "pk": False, "fk": None,                              "nullable": False, "description": "Row load timestamp."},
#         ],
#         "calculated_metrics": [
#             {"metric": "CPC",             "formula": "SUM(AMOUNT_SPENT_USD) / NULLIF(SUM(CLICKS), 0)",                              "description": "Cost Per Click. NOT a stored column — always calculate."},
#             {"metric": "CPM",             "formula": "(SUM(AMOUNT_SPENT_USD) / NULLIF(SUM(IMPRESSIONS), 0)) * 1000",                "description": "Cost Per 1000 Impressions. NOT a stored column — always calculate."},
#             {"metric": "TOTAL_SPEND",     "formula": "SUM(AMOUNT_SPENT_USD)",                                                       "description": "Total spend for the filtered period."},
#         ],
#         "relationships": [
#             "SPEND_DATE → DIM_DATE.DATE_KEY",
#             "CAMPAIGN_ID → DIM_CAMPAIGN.CAMPAIGN_ID",
#             "AD_GROUP_ID → DIM_AD_GROUP.AD_GROUP_ID",
#         ]
#     },

#     # ─────────────────────────────────────
#     #  TABLE 7 — FACT_CONVERSIONS
#     # ─────────────────────────────────────
#     {
#         "table": "FACT_CONVERSIONS",
#         "schema": "gold",
#         "description": "Conversion events attributed to ad campaigns. One row per conversion event. Use for ROAS, CPA, CVR queries.",
#         "grain": "One row per CONVERSION_ID",
#         "columns": [
#             {"column": "CONVERSION_ID",              "type": "VARCHAR(100)",  "pk": True,  "fk": None,                              "nullable": False, "description": "Primary key. Unique conversion event ID."},
#             {"column": "CONVERSION_DATE",            "type": "DATE",          "pk": False, "fk": "DIM_DATE.DATE_KEY",               "nullable": False, "description": "Date conversion occurred. FK to DIM_DATE.DATE_KEY."},
#             {"column": "CAMPAIGN_ID",                "type": "VARCHAR(50)",   "pk": False, "fk": "DIM_CAMPAIGN.CAMPAIGN_ID",        "nullable": False, "description": "FK to DIM_CAMPAIGN."},
#             {"column": "AD_GROUP_ID",                "type": "VARCHAR(50)",   "pk": False, "fk": "DIM_AD_GROUP.AD_GROUP_ID",        "nullable": True,  "description": "FK to DIM_AD_GROUP. NULL if not tracked at ad group level."},
#             {"column": "AD_CREATIVE_ID",             "type": "VARCHAR(50)",   "pk": False, "fk": "DIM_AD_CREATIVE.AD_CREATIVE_ID",  "nullable": True,  "description": "FK to DIM_AD_CREATIVE. NULL if not tracked at creative level."},
#             {"column": "PLATFORM",                   "type": "VARCHAR(50)",   "pk": False, "fk": None,                              "nullable": False, "description": "Attribution platform."},
#             {"column": "USER_ID",                    "type": "VARCHAR(100)",  "pk": False, "fk": None,                              "nullable": True,  "description": "Anonymized user identifier. NULL for non-logged-in users."},
#             {"column": "SESSION_ID",                 "type": "VARCHAR(100)",  "pk": False, "fk": "FACT_UTM_SESSIONS.SESSION_ID",    "nullable": True,  "description": "Web session ID at time of conversion. FK to FACT_UTM_SESSIONS."},
#             {"column": "CONVERSION_TYPE",            "type": "VARCHAR(100)",  "pk": False, "fk": None,                              "nullable": False, "description": "Type of conversion. Allowed values: 'PURCHASE', 'LEAD', 'SIGN_UP', 'DOWNLOAD', 'ADD_TO_CART', 'CHECKOUT_INITIATED', 'FORM_SUBMIT', 'CALL', 'APP_INSTALL'"},
#             {"column": "CONVERSION_VALUE_USD",       "type": "NUMBER(18,4)",  "pk": False, "fk": None,                              "nullable": False, "description": "Revenue value in USD. 0 for non-revenue events like LEAD, SIGN_UP. Filter WHERE CONVERSION_TYPE = 'PURCHASE' for revenue-only queries."},
#             {"column": "ATTRIBUTION_MODEL",          "type": "VARCHAR(50)",   "pk": False, "fk": None,                              "nullable": False, "description": "Attribution model used. Allowed values: 'LAST_CLICK', 'FIRST_CLICK', 'LINEAR', 'TIME_DECAY', 'DATA_DRIVEN'. ALWAYS filter on this to avoid double-counting."},
#             {"column": "ATTRIBUTION_WINDOW_DAYS",    "type": "NUMBER(3)",     "pk": False, "fk": None,                              "nullable": False, "description": "Attribution lookback window in days. Typical values: 7, 14, 30."},
#             {"column": "CLICK_TO_CONVERSION_DAYS",   "type": "NUMBER(5)",     "pk": False, "fk": None,                              "nullable": True,  "description": "Days elapsed between ad click and this conversion event."},
#             {"column": "CREATED_AT",                 "type": "TIMESTAMP_NTZ", "pk": False, "fk": None,                              "nullable": False, "description": "Row load timestamp."},
#         ],
#         "calculated_metrics": [
#             {"metric": "CVR",             "formula": "COUNT(CONVERSION_ID) / NULLIF(SUM(clicks_from_FACT_AD_PERFORMANCE), 0)",       "description": "Conversion Rate. Requires joining FACT_AD_PERFORMANCE for clicks denominator."},
#             {"metric": "CPA",             "formula": "SUM(AMOUNT_SPENT_USD from FACT_SPEND) / NULLIF(COUNT(CONVERSION_ID), 0)",      "description": "Cost Per Acquisition. Requires joining FACT_SPEND."},
#             {"metric": "ROAS",            "formula": "SUM(CONVERSION_VALUE_USD) / NULLIF(SUM(AMOUNT_SPENT_USD from FACT_SPEND), 0)", "description": "Return On Ad Spend. Requires joining FACT_SPEND. NOT a stored column."},
#         ],
#         "relationships": [
#             "CONVERSION_DATE → DIM_DATE.DATE_KEY",
#             "CAMPAIGN_ID → DIM_CAMPAIGN.CAMPAIGN_ID",
#             "AD_GROUP_ID → DIM_AD_GROUP.AD_GROUP_ID",
#             "AD_CREATIVE_ID → DIM_AD_CREATIVE.AD_CREATIVE_ID",
#             "SESSION_ID → FACT_UTM_SESSIONS.SESSION_ID",
#         ]
#     },

#     # ─────────────────────────────────────
#     #  TABLE 8 — FACT_UTM_SESSIONS
#     # ─────────────────────────────────────
#     {
#         "table": "FACT_UTM_SESSIONS",
#         "schema": "gold",
#         "description": "Web sessions with UTM tracking from Google Analytics / CDP. Links ad traffic to on-site behaviour.",
#         "grain": "One row per SESSION_ID",
#         "columns": [
#             {"column": "SESSION_ID",               "type": "VARCHAR(100)",  "pk": True,  "fk": None,                          "nullable": False, "description": "Primary key. Unique session identifier."},
#             {"column": "SESSION_DATE",             "type": "DATE",          "pk": False, "fk": "DIM_DATE.DATE_KEY",           "nullable": False, "description": "Date session started. FK to DIM_DATE.DATE_KEY."},
#             {"column": "USER_ID",                  "type": "VARCHAR(100)",  "pk": False, "fk": None,                          "nullable": True,  "description": "Anonymized user ID. NULL for anonymous sessions."},
#             {"column": "UTM_SOURCE",               "type": "VARCHAR(255)",  "pk": False, "fk": None,                          "nullable": True,  "description": "UTM source param. Examples: 'google', 'facebook', 'linkedin', 'email', 'organic'"},
#             {"column": "UTM_MEDIUM",               "type": "VARCHAR(255)",  "pk": False, "fk": None,                          "nullable": True,  "description": "UTM medium param. Examples: 'cpc', 'cpm', 'email', 'social', 'organic', 'referral'"},
#             {"column": "UTM_CAMPAIGN",             "type": "VARCHAR(255)",  "pk": False, "fk": None,                          "nullable": True,  "description": "UTM campaign param — stores CAMPAIGN_NAME string, NOT CAMPAIGN_ID. Do NOT join this directly to DIM_CAMPAIGN.CAMPAIGN_ID."},
#             {"column": "UTM_CONTENT",              "type": "VARCHAR(255)",  "pk": False, "fk": None,                          "nullable": True,  "description": "UTM content param (ad creative label). NULL if not set."},
#             {"column": "UTM_TERM",                 "type": "VARCHAR(255)",  "pk": False, "fk": None,                          "nullable": True,  "description": "UTM keyword/term param. NULL if not set."},
#             {"column": "LANDING_PAGE_URL",         "type": "VARCHAR(2000)", "pk": False, "fk": None,                          "nullable": True,  "description": "First page URL of the session."},
#             {"column": "DEVICE_TYPE",              "type": "VARCHAR(20)",   "pk": False, "fk": None,                          "nullable": True,  "description": "User device. Allowed values: 'DESKTOP', 'MOBILE', 'TABLET'"},
#             {"column": "BROWSER",                  "type": "VARCHAR(50)",   "pk": False, "fk": None,                          "nullable": True,  "description": "Browser name. Examples: 'Chrome', 'Safari', 'Firefox', 'Edge'"},
#             {"column": "COUNTRY_CODE",             "type": "VARCHAR(2)",    "pk": False, "fk": None,                          "nullable": True,  "description": "ISO 2-letter country code. Examples: 'IN', 'US', 'GB'"},
#             {"column": "CITY",                     "type": "VARCHAR(100)",  "pk": False, "fk": None,                          "nullable": True,  "description": "City name of the session user."},
#             {"column": "SESSION_DURATION_SECONDS", "type": "NUMBER(10)",    "pk": False, "fk": None,                          "nullable": True,  "description": "Total session duration in seconds."},
#             {"column": "PAGES_VIEWED",             "type": "NUMBER(5)",     "pk": False, "fk": None,                          "nullable": False, "description": "Number of pages viewed in this session."},
#             {"column": "BOUNCED",                  "type": "BOOLEAN",       "pk": False, "fk": None,                          "nullable": False, "description": "TRUE if user left after viewing only 1 page (bounce)."},
#             {"column": "CREATED_AT",               "type": "TIMESTAMP_NTZ", "pk": False, "fk": None,                          "nullable": False, "description": "Row load timestamp."},
#         ],
#         "relationships": [
#             "SESSION_DATE → DIM_DATE.DATE_KEY",
#             "SESSION_ID → FACT_CONVERSIONS.SESSION_ID",
#         ]
#     },
# ]

data_dict = [

    # ─────────────────────────────────────
    #  CORE FACT & DIMENSION TABLES
    # ─────────────────────────────────────
    {
        "table": "FACT_CAMPAIGN_PERFORMANCE",
        "schema": "GOLD",
        "description": "Core fact table storing daily performance metrics at the campaign, channel, company, and location grain.",
        "grain": "One row per (date, campaign_id, channel_used, company, location)",
        "columns": [
            {"column": "CAMPAIGN_ID",         "type": "NUMBER",    "description": "Foreign key linking to the campaign dimension."},
            {"column": "DATE",                "type": "TIMESTAMP", "description": "Date of the performance record."},
            {"column": "CHANNEL_USED",        "type": "STRING",    "description": "Marketing channel (e.g., Social, Search, Email)."},
            {"column": "COMPANY",             "type": "STRING",    "description": "Company associated with the campaign."},
            {"column": "LOCATION",            "type": "STRING",    "description": "Geographic location of the performance data."},
            {"column": "TOTAL_CLICKS",        "type": "NUMBER",    "description": "Total number of clicks generated."},
            {"column": "TOTAL_IMPRESSIONS",   "type": "NUMBER",    "description": "Total number of ad impressions."},
            {"column": "TOTAL_COST",          "type": "FLOAT",     "description": "Total spend/cost for the campaign on this date."},
            {"column": "AVG_CONVERSION_RATE", "type": "FLOAT",     "description": "Average conversion rate recorded for the day."},
            {"column": "AVG_ROI",             "type": "FLOAT",     "description": "Average Return on Investment for the day."},
            {"column": "AVG_CTR",             "type": "FLOAT",     "description": "Average Click-Through Rate for the day."}
        ]
    },
    {
        "table": "DIM_CAMPAIGN",
        "schema": "GOLD",
        "description": "Dimension table storing campaign metadata.",
        "columns": [
            {"column": "CAMPAIGN_ID",      "type": "NUMBER", "description": "Unique identifier for the campaign."},
            {"column": "CAMPAIGN_TYPE",    "type": "STRING", "description": "Type of the campaign (e.g., Awareness, Conversion)."},
            {"column": "TARGET_AUDIENCE",  "type": "STRING", "description": "Description of the target demographic."},
            {"column": "CUSTOMER_SEGMENT", "type": "STRING", "description": "Specific segment of customers targeted."}
        ]
    },
    {
        "table": "DIM_DATE",
        "schema": "GOLD",
        "description": "Calendar dimension table for time-based groupings.",
        "columns": [
            {"column": "DATE",       "type": "TIMESTAMP", "description": "Calendar date."},
            {"column": "YEAR",       "type": "NUMBER",    "description": "Year component of the date."},
            {"column": "MONTH",      "type": "NUMBER",    "description": "Numeric month (1-12)."},
            {"column": "MONTH_NAME", "type": "STRING",    "description": "Name of the month (e.g., 'January')."},
            {"column": "QUARTER",    "type": "NUMBER",    "description": "Quarter of the year (1-4)."}
        ]
    },
    {
        "table": "DIM_CHANNEL",
        "schema": "GOLD",
        "description": "Dimension table for marketing channels.",
        "columns": [{"column": "CHANNEL_USED", "type": "STRING", "description": "Distinct marketing channels available."}]
    },
    {
        "table": "DIM_COMPANY",
        "schema": "GOLD",
        "description": "Dimension table for companies.",
        "columns": [{"column": "COMPANY", "type": "STRING", "description": "Distinct companies associated with campaigns."}]
    },
    {
        "table": "DIM_LOCATION",
        "schema": "GOLD",
        "description": "Dimension table for target locations.",
        "columns": [{"column": "LOCATION", "type": "STRING", "description": "Distinct geographic locations."}]
    },

    # ─────────────────────────────────────
    #  PRE-AGGREGATED VIEWS (KPIs)
    # ─────────────────────────────────────
    {
        "table": "VW_KPI_SUMMARY",
        "schema": "GOLD",
        "description": "High-level aggregate view of all-time overall performance. Use for dashboard top-line numbers.",
        "columns": [
            {"column": "TOTAL_CLICKS",      "type": "NUMBER", "description": "All-time total clicks."},
            {"column": "TOTAL_IMPRESSIONS", "type": "NUMBER", "description": "All-time total impressions."},
            {"column": "TOTAL_COST",        "type": "FLOAT",  "description": "All-time total cost."},
            {"column": "CTR",               "type": "FLOAT",  "description": "Overall weighted Click-Through Rate."},
            {"column": "AVG_ROI",           "type": "FLOAT",  "description": "Overall average Return on Investment."}
        ]
    },
    {
        "table": "VW_CHANNEL_PERFORMANCE",
        "schema": "GOLD",
        "description": "Daily performance aggregated by marketing channel.",
        "columns": [
            {"column": "DATE",              "type": "TIMESTAMP", "description": "Date of the record."},
            {"column": "CHANNEL_USED",      "type": "STRING",    "description": "Marketing channel."},
            {"column": "TOTAL_CLICKS",      "type": "NUMBER",    "description": "Total clicks for the channel on this date."},
            {"column": "TOTAL_IMPRESSIONS", "type": "NUMBER",    "description": "Total impressions for the channel on this date."},
            {"column": "CTR",               "type": "FLOAT",     "description": "Weighted CTR for the channel on this date."},
            {"column": "AVG_ROI",           "type": "FLOAT",     "description": "Average ROI for the channel on this date."}
        ]
    },
    {
        "table": "VW_CAMPAIGN_SUMMARY",
        "schema": "GOLD",
        "description": "All-time performance aggregated by campaign ID.",
        "columns": [
            {"column": "CAMPAIGN_ID",       "type": "NUMBER", "description": "Unique campaign identifier."},
            {"column": "TOTAL_CLICKS",      "type": "NUMBER", "description": "Total clicks for this campaign."},
            {"column": "TOTAL_IMPRESSIONS", "type": "NUMBER", "description": "Total impressions for this campaign."},
            {"column": "TOTAL_COST",        "type": "FLOAT",  "description": "Total cost spent on this campaign."},
            {"column": "CTR",               "type": "FLOAT",  "description": "Weighted CTR for this campaign."},
            {"column": "AVG_ROI",           "type": "FLOAT",  "description": "Average ROI for this campaign."}
        ]
    },
    {
        "table": "VW_MONTHLY_TRENDS",
        "schema": "GOLD",
        "description": "Performance aggregated by year and month. Use for month-over-month trend analysis.",
        "columns": [
            {"column": "YEAR",              "type": "NUMBER", "description": "Year of the record."},
            {"column": "MONTH",             "type": "NUMBER", "description": "Numeric month (1-12)."},
            {"column": "TOTAL_CLICKS",      "type": "NUMBER", "description": "Total clicks for the month."},
            {"column": "TOTAL_IMPRESSIONS", "type": "NUMBER", "description": "Total impressions for the month."},
            {"column": "CTR",               "type": "FLOAT",  "description": "Weighted CTR for the month."},
            {"column": "AVG_ROI",           "type": "FLOAT",  "description": "Average ROI for the month."}
        ]
    },
    {
        "table": "VW_CAMPAIGN_PERFORMANCE",
        "schema": "GOLD",
        "description": "Master flattened view combining FACT_CAMPAIGN_PERFORMANCE, DIM_CAMPAIGN, and DIM_DATE. Use when filtering by specific demographics, company, or location.",
        "columns": [
            {"column": "CAMPAIGN_ID",         "type": "NUMBER",    "description": "Unique identifier for the campaign."},
            {"column": "DATE",                "type": "TIMESTAMP", "description": "Date of the performance record."},
            {"column": "YEAR",                "type": "NUMBER",    "description": "Year of the record."},
            {"column": "MONTH",               "type": "NUMBER",    "description": "Numeric month of the record."},
            {"column": "MONTH_NAME",          "type": "STRING",    "description": "Name of the month."},
            {"column": "QUARTER",             "type": "NUMBER",    "description": "Quarter of the year."},
            {"column": "CHANNEL_USED",        "type": "STRING",    "description": "Marketing channel."},
            {"column": "COMPANY",             "type": "STRING",    "description": "Company associated with the campaign."},
            {"column": "LOCATION",            "type": "STRING",    "description": "Geographic location."},
            {"column": "CAMPAIGN_TYPE",       "type": "STRING",    "description": "Type of the campaign."},
            {"column": "TARGET_AUDIENCE",     "type": "STRING",    "description": "Target demographic."},
            {"column": "CUSTOMER_SEGMENT",    "type": "STRING",    "description": "Specific segment of customers targeted."},
            {"column": "TOTAL_CLICKS",        "type": "NUMBER",    "description": "Total clicks generated."},
            {"column": "TOTAL_IMPRESSIONS",   "type": "NUMBER",    "description": "Total ad impressions."},
            {"column": "TOTAL_COST",          "type": "FLOAT",     "description": "Total cost spent."},
            {"column": "AVG_CONVERSION_RATE", "type": "FLOAT",     "description": "Average conversion rate."},
            {"column": "AVG_ROI",             "type": "FLOAT",     "description": "Average Return on Investment."},
            {"column": "AVG_CTR",             "type": "FLOAT",     "description": "Average Click-Through Rate."}
        ]
    }
]

# ============================================================
#  BUSINESS RULES — inject this into your system prompt too
# ============================================================

business_rules = [
  
    "Whenever a user asks for overall, high-level metrics, query VW_KPI_SUMMARY.",
    "Whenever a user asks for monthly trends or month-over-month comparisons, query VW_MONTHLY_TRENDS.",
    "Whenever a user asks for channel-specific aggregate performance, query VW_CHANNEL_PERFORMANCE.",
    "Whenever a user asks for campaign-specific aggregate performance, query VW_CAMPAIGN_SUMMARY.",
    "If a query requires filtering by Company, Location, Campaign Type, or Target Audience, use the flattened master view VW_CAMPAIGN_PERFORMANCE.",
    "All table and view names MUST be fully qualified with the database and schema name. Example: MARKETING_ANALYTICS.GOLD.VW_MONTHLY_TRENDS",
    "Never use SELECT *. Always select specific columns."

    "CTR, ROAS, CPA, CVR, CPC, CPM are NEVER stored columns. Always calculate them using the formulas in calculated_metrics.",
    "For month-wise aggregation ALWAYS use DATE_TRUNC('MONTH', <date_column>) in Snowflake. Never use MONTH() or EXTRACT(MONTH FROM ...).",
    "FACT_AD_PERFORMANCE and FACT_SPEND are separate tables. Never join them directly on a date without pre-aggregating first — direct joins cause row fan-out and wrong numbers.",
    "CONVERSION_VALUE_USD = 0 for non-revenue types like LEAD and SIGN_UP. For revenue queries always add: WHERE CONVERSION_TYPE = 'PURCHASE'.",
    "FACT_CONVERSIONS can have multiple rows per real conversion if multiple ATTRIBUTION_MODEL values are tracked. Always filter: WHERE ATTRIBUTION_MODEL = 'LAST_CLICK' (or the model requested) to avoid double counting.",
    "REACH and IMPRESSIONS are different. IMPRESSIONS = total ad shows (one user can see ad 10 times = 10 impressions). REACH = unique users who saw the ad.",
    "VIDEO_VIEWS, VIDEO_VIEW_25_PCT, VIDEO_VIEW_50_PCT, VIDEO_VIEW_75_PCT, VIDEO_VIEW_100_PCT are NULL (not 0) for non-video ad formats. Always use COALESCE(<col>, 0) when aggregating across mixed formats.",
    "UTM_CAMPAIGN in FACT_UTM_SESSIONS stores campaign NAME (string), not CAMPAIGN_ID. Do NOT join FACT_UTM_SESSIONS.UTM_CAMPAIGN to DIM_CAMPAIGN.CAMPAIGN_ID.",
    "PLATFORM is denormalized into all FACT tables. You do NOT need to join DIM_CAMPAIGN just to filter by platform.",
    "All monetary values (AMOUNT_SPENT_USD, CONVERSION_VALUE_USD, BID_AMOUNT_USD) are already in USD. Never apply exchange rate logic.",
    "Always use NULLIF(denominator, 0) in division to avoid Snowflake divide-by-zero errors.",
    "Never use SELECT *. Always name columns explicitly in generated SQL.",
    "All table names must be fully qualified as gold.<TABLE_NAME> in every query.",
]


# ============================================================
#  QUERY PATTERNS — inject as few-shot examples
# ============================================================

query_patterns = [
    {
        "user_ask": "What is our overall total spend, clicks, and CTR across all campaigns?",
        "sql": """
SELECT
    TOTAL_COST,
    TOTAL_CLICKS,
    CTR
FROM MARKETING_ANALYTICS.GOLD.VW_KPI_SUMMARY;
"""
    },
    {
        "user_ask": "How did our marketing channels perform over time? Show me the daily clicks and ROI by channel.",
        "sql": """
SELECT
    DATE,
    CHANNEL_USED,
    TOTAL_CLICKS,
    AVG_ROI
FROM MARKETING_ANALYTICS.GOLD.VW_CHANNEL_PERFORMANCE
ORDER BY DATE DESC, TOTAL_CLICKS DESC;
"""
    },
    {
        "user_ask": "Show me the month-by-month trend for our total impressions and average CTR.",
        "sql": """
SELECT
    YEAR,
    MONTH,
    TOTAL_IMPRESSIONS,
    CTR
FROM MARKETING_ANALYTICS.GOLD.VW_MONTHLY_TRENDS
ORDER BY YEAR DESC, MONTH DESC;
"""
    },
    {
        "user_ask": "Which top 5 campaigns have driven the most clicks, and what is their cost?",
        "sql": """
SELECT
    CAMPAIGN_ID,
    TOTAL_CLICKS,
    TOTAL_COST,
    CTR
FROM MARKETING_ANALYTICS.GOLD.VW_CAMPAIGN_SUMMARY
ORDER BY TOTAL_CLICKS DESC
LIMIT 5;
"""
    },
    {
        "user_ask": "What is the total spend and overall CTR grouped by campaign type and target audience?",
        "sql": """
SELECT
    CAMPAIGN_TYPE,
    TARGET_AUDIENCE,
    SUM(TOTAL_COST) AS TOTAL_SPEND,
    SUM(TOTAL_CLICKS) AS TOTAL_CLICKS,
    CASE 
        WHEN SUM(TOTAL_IMPRESSIONS) > 0 THEN SUM(TOTAL_CLICKS) / SUM(TOTAL_IMPRESSIONS) 
        ELSE 0 
    END AS AGGREGATED_CTR
FROM MARKETING_ANALYTICS.GOLD.VW_CAMPAIGN_PERFORMANCE
GROUP BY CAMPAIGN_TYPE, TARGET_AUDIENCE
ORDER BY TOTAL_SPEND DESC;
"""
    },
    {
        "user_ask": "List all the distinct marketing channels we are tracking.",
        "sql": """
SELECT 
    CHANNEL_USED 
FROM MARKETING_ANALYTICS.GOLD.DIM_CHANNEL;
"""
    }
]


# def build_system_prompt(data_dict, business_rules, query_patterns):
#     prompt = "You are a Snowflake SQL expert for a marketing analytics data warehouse.\n\n"
#     prompt += "## STRICT RULES\n"
#     for i, rule in enumerate(business_rules, 1):
#         prompt += f"{i}. {rule}\n"

#     prompt += "\n## DATA DICTIONARY\n"
#     for table in data_dict:
#         prompt += f"\n### TABLE: {table['schema']}.{table['table']}\n"
#         prompt += f"Description: {table['description']}\n"
#         prompt += f"Grain: {table['grain']}\n"
#         prompt += "Columns:\n"
#         for col in table["columns"]:
#             fk_note = f" | FK → {col['fk']}" if col["fk"] else ""
#             null_note = " | NULLABLE" if col["nullable"] else " | NOT NULL"
#             prompt += f"  - {col['column']} ({col['type']}){fk_note}{null_note}: {col['description']}\n"
#         if "calculated_metrics" in table:
#             prompt += "Calculated Metrics (NOT stored columns):\n"
#             for m in table["calculated_metrics"]:
#                 prompt += f"  - {m['metric']} = {m['formula']}  → {m['description']}\n"

#     prompt += "\n## EXAMPLE QUERY PATTERNS\n"
#     for qp in query_patterns:
#         prompt += f"\nUser asks: \"{qp['user_ask']}\"\nSQL:\n{qp['sql']}\n"

#     return prompt

# def build_system_prompt(data_dict, business_rules, query_patterns):
#     prompt = "You are a Snowflake SQL expert for a marketing analytics data warehouse.\n\n"
#     prompt += "## STRICT RULES\n"
#     for i, rule in enumerate(business_rules, 1):
#         prompt += f"{i}. {rule}\n"

#     prompt += "\n## DATA DICTIONARY\n"
#     for table in data_dict:
#         prompt += f"\n### TABLE: {table.get('schema', 'GOLD')}.{table.get('table')}\n"
#         prompt += f"Description: {table.get('description', '')}\n"
        
#         # Safely get 'grain' only if it exists
#         if table.get('grain'):
#             prompt += f"Grain: {table.get('grain')}\n"
            
#         prompt += "Columns:\n"
#         for col in table.get("columns", []):
#             # Safely get 'fk' and 'nullable' using .get() so it doesn't crash if missing
#             fk_val = col.get("fk")
#             fk_note = f" | FK → {fk_val}" if fk_val else ""
            
#             null_val = col.get("nullable")
#             null_note = ""
#             if null_val is not None:
#                 null_note = " | NULLABLE" if null_val else " | NOT NULL"
                
#             prompt += f"  - {col.get('column')} ({col.get('type')}){fk_note}{null_note}: {col.get('description', '')}\n"
            
#         # Safely handle calculated metrics if we ever add them back
#         if "calculated_metrics" in table:
#             prompt += "Calculated Metrics (NOT stored columns):\n"
#             for m in table["calculated_metrics"]:
#                 prompt += f"  - {m['metric']} = {m['formula']}  → {m['description']}\n"

#     prompt += "\n## EXAMPLE QUERY PATTERNS\n"
#     for qp in query_patterns:
#         prompt += f"\nUser asks: \"{qp['user_ask']}\"\nSQL:\n{qp['sql']}\n"

#     return prompt