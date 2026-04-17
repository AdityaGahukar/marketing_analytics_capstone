
data_dict = [

    # ─────────────────────────────────────
    #  TABLE 1 — DIM_CAMPAIGN
    # ─────────────────────────────────────
    {
        "table": "DIM_CAMPAIGN",
        "schema": "gold",
        "description": "Master dimension for all marketing campaigns. One row per campaign.",
        "grain": "One row per CAMPAIGN_ID",
        "columns": [
            {"column": "CAMPAIGN_ID",          "type": "VARCHAR(50)",   "pk": True,  "fk": None,                              "nullable": False, "description": "Primary key. Unique campaign ID from ad platform."},
            {"column": "CAMPAIGN_NAME",        "type": "VARCHAR(255)",  "pk": False, "fk": None,                              "nullable": False, "description": "Human-readable campaign name as set in the ad platform."},
            {"column": "PLATFORM",             "type": "VARCHAR(50)",   "pk": False, "fk": None,                              "nullable": False, "description": "Ad platform. Allowed values: 'GOOGLE', 'META', 'LINKEDIN', 'TWITTER', 'TIKTOK', 'EMAIL', 'ORGANIC'"},
            {"column": "CAMPAIGN_TYPE",        "type": "VARCHAR(50)",   "pk": False, "fk": None,                              "nullable": True,  "description": "Campaign type. Allowed values: 'SEARCH', 'DISPLAY', 'VIDEO', 'SHOPPING', 'SOCIAL', 'EMAIL', 'RETARGETING'"},
            {"column": "CAMPAIGN_OBJECTIVE",   "type": "VARCHAR(100)",  "pk": False, "fk": None,                              "nullable": True,  "description": "Campaign goal. Allowed values: 'BRAND_AWARENESS', 'LEAD_GENERATION', 'CONVERSIONS', 'TRAFFIC', 'ENGAGEMENT', 'RETENTION'"},
            {"column": "CAMPAIGN_STATUS",      "type": "VARCHAR(20)",   "pk": False, "fk": None,                              "nullable": False, "description": "Status. Allowed values: 'ACTIVE', 'PAUSED', 'ENDED', 'DRAFT'"},
            {"column": "START_DATE",           "type": "DATE",          "pk": False, "fk": None,                              "nullable": False, "description": "Campaign start date (YYYY-MM-DD)."},
            {"column": "END_DATE",             "type": "DATE",          "pk": False, "fk": None,                              "nullable": True,  "description": "Campaign end date. NULL if campaign is still ongoing."},
            {"column": "TARGET_AUDIENCE",      "type": "VARCHAR(255)",  "pk": False, "fk": None,                              "nullable": True,  "description": "Free-text description of the target audience segment."},
            {"column": "TARGET_GEOGRAPHY",     "type": "VARCHAR(255)",  "pk": False, "fk": None,                              "nullable": True,  "description": "Targeted geographic regions, comma-separated."},
            {"column": "BUDGET_TYPE",          "type": "VARCHAR(20)",   "pk": False, "fk": None,                              "nullable": True,  "description": "Budget cadence. Allowed values: 'DAILY', 'LIFETIME', 'MONTHLY'"},
            {"column": "TOTAL_BUDGET_USD",     "type": "NUMBER(18,2)",  "pk": False, "fk": None,                              "nullable": True,  "description": "Total allocated budget in USD."},
            {"column": "CREATED_AT",           "type": "TIMESTAMP_NTZ", "pk": False, "fk": None,                              "nullable": False, "description": "Row creation timestamp."},
            {"column": "UPDATED_AT",           "type": "TIMESTAMP_NTZ", "pk": False, "fk": None,                              "nullable": False, "description": "Row last updated timestamp."},
        ],
        "relationships": [
            "CAMPAIGN_ID → FACT_AD_PERFORMANCE.CAMPAIGN_ID",
            "CAMPAIGN_ID → FACT_SPEND.CAMPAIGN_ID",
            "CAMPAIGN_ID → FACT_CONVERSIONS.CAMPAIGN_ID",
        ]
    },

    # ─────────────────────────────────────
    #  TABLE 2 — DIM_AD_GROUP
    # ─────────────────────────────────────
    {
        "table": "DIM_AD_GROUP",
        "schema": "gold",
        "description": "Ad groups or ad sets within a campaign. Child of DIM_CAMPAIGN.",
        "grain": "One row per AD_GROUP_ID",
        "columns": [
            {"column": "AD_GROUP_ID",          "type": "VARCHAR(50)",   "pk": True,  "fk": None,                              "nullable": False, "description": "Primary key. Unique ad group / ad set ID."},
            {"column": "AD_GROUP_NAME",        "type": "VARCHAR(255)",  "pk": False, "fk": None,                              "nullable": False, "description": "Name of the ad group or ad set."},
            {"column": "CAMPAIGN_ID",          "type": "VARCHAR(50)",   "pk": False, "fk": "DIM_CAMPAIGN.CAMPAIGN_ID",        "nullable": False, "description": "Foreign key to DIM_CAMPAIGN."},
            {"column": "BID_STRATEGY",         "type": "VARCHAR(100)",  "pk": False, "fk": None,                              "nullable": True,  "description": "Bidding strategy. Allowed values: 'CPC', 'CPM', 'CPA', 'ROAS_TARGET', 'MANUAL_CPC', 'ENHANCED_CPC', 'TARGET_IMPRESSION_SHARE'"},
            {"column": "BID_AMOUNT_USD",       "type": "NUMBER(18,4)",  "pk": False, "fk": None,                              "nullable": True,  "description": "Manual bid amount in USD. NULL when automated bidding is used."},
            {"column": "AD_GROUP_STATUS",      "type": "VARCHAR(20)",   "pk": False, "fk": None,                              "nullable": False, "description": "Status. Allowed values: 'ACTIVE', 'PAUSED', 'REMOVED'"},
            {"column": "TARGETING_TYPE",       "type": "VARCHAR(50)",   "pk": False, "fk": None,                              "nullable": True,  "description": "Audience targeting method. Allowed values: 'KEYWORD', 'INTEREST', 'LOOKALIKE', 'REMARKETING', 'DEMOGRAPHIC', 'CONTEXTUAL'"},
            {"column": "CREATED_AT",           "type": "TIMESTAMP_NTZ", "pk": False, "fk": None,                              "nullable": False, "description": "Row creation timestamp."},
            {"column": "UPDATED_AT",           "type": "TIMESTAMP_NTZ", "pk": False, "fk": None,                              "nullable": False, "description": "Row last updated timestamp."},
        ],
        "relationships": [
            "AD_GROUP_ID → FACT_AD_PERFORMANCE.AD_GROUP_ID",
            "CAMPAIGN_ID → DIM_CAMPAIGN.CAMPAIGN_ID",
        ]
    },

    # ─────────────────────────────────────
    #  TABLE 3 — DIM_AD_CREATIVE
    # ─────────────────────────────────────
    {
        "table": "DIM_AD_CREATIVE",
        "schema": "gold",
        "description": "Individual ad creatives — the actual ads shown to users.",
        "grain": "One row per AD_CREATIVE_ID",
        "columns": [
            {"column": "AD_CREATIVE_ID",       "type": "VARCHAR(50)",   "pk": True,  "fk": None,                              "nullable": False, "description": "Primary key. Unique ad creative ID."},
            {"column": "AD_GROUP_ID",          "type": "VARCHAR(50)",   "pk": False, "fk": "DIM_AD_GROUP.AD_GROUP_ID",        "nullable": False, "description": "Foreign key to DIM_AD_GROUP."},
            {"column": "CAMPAIGN_ID",          "type": "VARCHAR(50)",   "pk": False, "fk": "DIM_CAMPAIGN.CAMPAIGN_ID",        "nullable": False, "description": "Denormalized FK to DIM_CAMPAIGN for query convenience."},
            {"column": "AD_NAME",              "type": "VARCHAR(255)",  "pk": False, "fk": None,                              "nullable": False, "description": "Label or name of the ad creative."},
            {"column": "AD_FORMAT",            "type": "VARCHAR(50)",   "pk": False, "fk": None,                              "nullable": False, "description": "Creative format. Allowed values: 'IMAGE', 'VIDEO', 'CAROUSEL', 'TEXT', 'RESPONSIVE', 'STORY', 'REEL', 'HTML5'"},
            {"column": "HEADLINE",             "type": "VARCHAR(500)",  "pk": False, "fk": None,                              "nullable": True,  "description": "Primary headline text of the ad."},
            {"column": "DESCRIPTION",          "type": "VARCHAR(1000)", "pk": False, "fk": None,                              "nullable": True,  "description": "Body/description text of the ad."},
            {"column": "CALL_TO_ACTION",       "type": "VARCHAR(100)",  "pk": False, "fk": None,                              "nullable": True,  "description": "CTA button text. Examples: 'LEARN_MORE', 'SIGN_UP', 'BUY_NOW', 'GET_QUOTE', 'DOWNLOAD'"},
            {"column": "DESTINATION_URL",      "type": "VARCHAR(2000)", "pk": False, "fk": None,                              "nullable": True,  "description": "Final landing page URL without tracking parameters."},
            {"column": "CREATIVE_STATUS",      "type": "VARCHAR(20)",   "pk": False, "fk": None,                              "nullable": False, "description": "Status. Allowed values: 'ACTIVE', 'PAUSED', 'DISAPPROVED', 'ARCHIVED'"},
            {"column": "CREATED_AT",           "type": "TIMESTAMP_NTZ", "pk": False, "fk": None,                              "nullable": False, "description": "Row creation timestamp."},
            {"column": "UPDATED_AT",           "type": "TIMESTAMP_NTZ", "pk": False, "fk": None,                              "nullable": False, "description": "Row last updated timestamp."},
        ],
        "relationships": [
            "AD_CREATIVE_ID → FACT_AD_PERFORMANCE.AD_CREATIVE_ID",
            "AD_GROUP_ID → DIM_AD_GROUP.AD_GROUP_ID",
        ]
    },

    # ─────────────────────────────────────
    #  TABLE 4 — DIM_DATE
    # ─────────────────────────────────────
    {
        "table": "DIM_DATE",
        "schema": "gold",
        "description": "Calendar date dimension. One row per day. Use for all date filtering and grouping.",
        "grain": "One row per DATE_KEY (calendar day)",
        "columns": [
            {"column": "DATE_KEY",             "type": "DATE",          "pk": True,  "fk": None,  "nullable": False, "description": "Primary key. Calendar date in YYYY-MM-DD format."},
            {"column": "DAY_OF_WEEK",          "type": "VARCHAR(10)",   "pk": False, "fk": None,  "nullable": False, "description": "Full day name. Values: 'Monday' through 'Sunday'"},
            {"column": "DAY_OF_WEEK_NUM",      "type": "NUMBER(1)",     "pk": False, "fk": None,  "nullable": False, "description": "Day number. 1=Sunday ... 7=Saturday (Snowflake DAYOFWEEK convention)."},
            {"column": "DAY_OF_MONTH",         "type": "NUMBER(2)",     "pk": False, "fk": None,  "nullable": False, "description": "Day of month (1–31)."},
            {"column": "WEEK_OF_YEAR",         "type": "NUMBER(2)",     "pk": False, "fk": None,  "nullable": False, "description": "ISO week number (1–53)."},
            {"column": "MONTH_NUM",            "type": "NUMBER(2)",     "pk": False, "fk": None,  "nullable": False, "description": "Month number (1–12)."},
            {"column": "MONTH_NAME",           "type": "VARCHAR(10)",   "pk": False, "fk": None,  "nullable": False, "description": "Full month name. Values: 'January' through 'December'"},
            {"column": "MONTH_SHORT",          "type": "VARCHAR(3)",    "pk": False, "fk": None,  "nullable": False, "description": "3-letter month abbreviation: 'Jan', 'Feb', ... 'Dec'"},
            {"column": "QUARTER",              "type": "NUMBER(1)",     "pk": False, "fk": None,  "nullable": False, "description": "Quarter number (1–4)."},
            {"column": "YEAR",                 "type": "NUMBER(4)",     "pk": False, "fk": None,  "nullable": False, "description": "4-digit year."},
            {"column": "YEAR_MONTH",           "type": "VARCHAR(7)",    "pk": False, "fk": None,  "nullable": False, "description": "Month label formatted as 'YYYY-MM'. Use this for month-wise display in results."},
            {"column": "IS_WEEKEND",           "type": "BOOLEAN",       "pk": False, "fk": None,  "nullable": False, "description": "TRUE if Saturday or Sunday."},
            {"column": "IS_HOLIDAY",           "type": "BOOLEAN",       "pk": False, "fk": None,  "nullable": False, "description": "TRUE if a public holiday (India + US calendar)."},
        ],
        "relationships": [
            "DATE_KEY → FACT_AD_PERFORMANCE.EVENT_DATE",
            "DATE_KEY → FACT_SPEND.SPEND_DATE",
            "DATE_KEY → FACT_CONVERSIONS.CONVERSION_DATE",
        ]
    },

    # ─────────────────────────────────────
    #  TABLE 5 — FACT_AD_PERFORMANCE
    # ─────────────────────────────────────
    {
        "table": "FACT_AD_PERFORMANCE",
        "schema": "gold",
        "description": "Core daily performance fact table. One row per (date, campaign, ad_group, ad_creative, platform). Primary table for CTR, impressions, clicks queries.",
        "grain": "Daily — one row per (EVENT_DATE, CAMPAIGN_ID, AD_GROUP_ID, AD_CREATIVE_ID, PLATFORM)",
        "columns": [
            {"column": "PERFORMANCE_ID",       "type": "VARCHAR(100)",  "pk": True,  "fk": None,                                    "nullable": False, "description": "Surrogate PK. Hash of grain columns."},
            {"column": "EVENT_DATE",           "type": "DATE",          "pk": False, "fk": "DIM_DATE.DATE_KEY",                     "nullable": False, "description": "Date of the performance data. FK to DIM_DATE.DATE_KEY."},
            {"column": "CAMPAIGN_ID",          "type": "VARCHAR(50)",   "pk": False, "fk": "DIM_CAMPAIGN.CAMPAIGN_ID",              "nullable": False, "description": "FK to DIM_CAMPAIGN."},
            {"column": "AD_GROUP_ID",          "type": "VARCHAR(50)",   "pk": False, "fk": "DIM_AD_GROUP.AD_GROUP_ID",              "nullable": False, "description": "FK to DIM_AD_GROUP."},
            {"column": "AD_CREATIVE_ID",       "type": "VARCHAR(50)",   "pk": False, "fk": "DIM_AD_CREATIVE.AD_CREATIVE_ID",        "nullable": True,  "description": "FK to DIM_AD_CREATIVE. NULL if not tracked at creative level."},
            {"column": "PLATFORM",             "type": "VARCHAR(50)",   "pk": False, "fk": None,                                    "nullable": False, "description": "Denormalized platform name. Allowed values: 'GOOGLE', 'META', 'LINKEDIN', 'TWITTER', 'TIKTOK', 'EMAIL', 'ORGANIC'"},
            {"column": "IMPRESSIONS",          "type": "NUMBER(18,0)",  "pk": False, "fk": None,                                    "nullable": False, "description": "Total times the ad was shown. One user can generate multiple impressions."},
            {"column": "CLICKS",               "type": "NUMBER(18,0)",  "pk": False, "fk": None,                                    "nullable": False, "description": "Total clicks on the ad."},
            {"column": "VIDEO_VIEWS",          "type": "NUMBER(18,0)",  "pk": False, "fk": None,                                    "nullable": True,  "description": "Total video views. NULL for non-video ad formats. Use COALESCE(VIDEO_VIEWS, 0) when aggregating."},
            {"column": "VIDEO_VIEW_25_PCT",    "type": "NUMBER(18,0)",  "pk": False, "fk": None,                                    "nullable": True,  "description": "Users who watched at least 25% of the video. NULL for non-video."},
            {"column": "VIDEO_VIEW_50_PCT",    "type": "NUMBER(18,0)",  "pk": False, "fk": None,                                    "nullable": True,  "description": "Users who watched at least 50% of the video. NULL for non-video."},
            {"column": "VIDEO_VIEW_75_PCT",    "type": "NUMBER(18,0)",  "pk": False, "fk": None,                                    "nullable": True,  "description": "Users who watched at least 75% of the video. NULL for non-video."},
            {"column": "VIDEO_VIEW_100_PCT",   "type": "NUMBER(18,0)",  "pk": False, "fk": None,                                    "nullable": True,  "description": "Users who watched the full video. NULL for non-video."},
            {"column": "REACH",                "type": "NUMBER(18,0)",  "pk": False, "fk": None,                                    "nullable": True,  "description": "Unique users who saw the ad. REACH != IMPRESSIONS. One user can have many impressions but only 1 reach."},
            {"column": "FREQUENCY",            "type": "NUMBER(10,4)",  "pk": False, "fk": None,                                    "nullable": True,  "description": "Average times a unique user saw the ad. = IMPRESSIONS / REACH"},
            {"column": "ENGAGEMENTS",          "type": "NUMBER(18,0)",  "pk": False, "fk": None,                                    "nullable": True,  "description": "Total social engagements: likes, shares, comments, saves combined."},
            {"column": "LINK_CLICKS",          "type": "NUMBER(18,0)",  "pk": False, "fk": None,                                    "nullable": True,  "description": "Clicks specifically on the CTA link. Subset of CLICKS. Use for landing page traffic analysis."},
            {"column": "POST_CLICK_SESSIONS",  "type": "NUMBER(18,0)",  "pk": False, "fk": None,                                    "nullable": True,  "description": "Website sessions attributed to an ad click (sourced from analytics platform)."},
            {"column": "CREATED_AT",           "type": "TIMESTAMP_NTZ", "pk": False, "fk": None,                                    "nullable": False, "description": "Row load timestamp."},
        ],
        "calculated_metrics": [
            {"metric": "CTR",             "formula": "SUM(CLICKS) / NULLIF(SUM(IMPRESSIONS), 0)",                                   "description": "Click-Through Rate. NOT a stored column — always calculate."},
            {"metric": "CTR_PERCENT",     "formula": "ROUND(SUM(CLICKS) / NULLIF(SUM(IMPRESSIONS), 0) * 100, 4)",                   "description": "CTR expressed as percentage."},
            {"metric": "VTR",             "formula": "SUM(VIDEO_VIEWS) / NULLIF(SUM(IMPRESSIONS), 0)",                              "description": "Video View-Through Rate. Only meaningful for VIDEO format."},
            {"metric": "ENGAGEMENT_RATE", "formula": "SUM(ENGAGEMENTS) / NULLIF(SUM(IMPRESSIONS), 0)",                              "description": "Engagement Rate. NOT a stored column — always calculate."},
            {"metric": "LINK_CTR",        "formula": "SUM(LINK_CLICKS) / NULLIF(SUM(IMPRESSIONS), 0)",                              "description": "Link Click-Through Rate. NOT a stored column — always calculate."},
        ],
        "relationships": [
            "EVENT_DATE → DIM_DATE.DATE_KEY",
            "CAMPAIGN_ID → DIM_CAMPAIGN.CAMPAIGN_ID",
            "AD_GROUP_ID → DIM_AD_GROUP.AD_GROUP_ID",
            "AD_CREATIVE_ID → DIM_AD_CREATIVE.AD_CREATIVE_ID",
        ]
    },

    # ─────────────────────────────────────
    #  TABLE 6 — FACT_SPEND
    # ─────────────────────────────────────
    {
        "table": "FACT_SPEND",
        "schema": "gold",
        "description": "Daily ad spend fact table. One row per (date, campaign, ad_group, platform). Use for budget, cost, CPM, CPC analysis.",
        "grain": "Daily — one row per (SPEND_DATE, CAMPAIGN_ID, AD_GROUP_ID, PLATFORM)",
        "columns": [
            {"column": "SPEND_ID",             "type": "VARCHAR(100)",  "pk": True,  "fk": None,                              "nullable": False, "description": "Surrogate PK."},
            {"column": "SPEND_DATE",           "type": "DATE",          "pk": False, "fk": "DIM_DATE.DATE_KEY",               "nullable": False, "description": "Date of the spend. FK to DIM_DATE.DATE_KEY."},
            {"column": "CAMPAIGN_ID",          "type": "VARCHAR(50)",   "pk": False, "fk": "DIM_CAMPAIGN.CAMPAIGN_ID",        "nullable": False, "description": "FK to DIM_CAMPAIGN."},
            {"column": "AD_GROUP_ID",          "type": "VARCHAR(50)",   "pk": False, "fk": "DIM_AD_GROUP.AD_GROUP_ID",        "nullable": True,  "description": "FK to DIM_AD_GROUP. NULL if spend is only tracked at campaign level."},
            {"column": "PLATFORM",             "type": "VARCHAR(50)",   "pk": False, "fk": None,                              "nullable": False, "description": "Denormalized platform name."},
            {"column": "AMOUNT_SPENT_USD",     "type": "NUMBER(18,4)",  "pk": False, "fk": None,                              "nullable": False, "description": "Actual amount spent on this date in USD. Already converted from source currency."},
            {"column": "IMPRESSIONS",          "type": "NUMBER(18,0)",  "pk": False, "fk": None,                              "nullable": False, "description": "Impressions on this date. Used for CPM calculation."},
            {"column": "CLICKS",               "type": "NUMBER(18,0)",  "pk": False, "fk": None,                              "nullable": False, "description": "Clicks on this date. Used for CPC calculation."},
            {"column": "CURRENCY_CODE",        "type": "VARCHAR(3)",    "pk": False, "fk": None,                              "nullable": False, "description": "Original source currency code e.g. 'USD', 'INR'. Conversion already applied in AMOUNT_SPENT_USD."},
            {"column": "CREATED_AT",           "type": "TIMESTAMP_NTZ", "pk": False, "fk": None,                              "nullable": False, "description": "Row load timestamp."},
        ],
        "calculated_metrics": [
            {"metric": "CPC",             "formula": "SUM(AMOUNT_SPENT_USD) / NULLIF(SUM(CLICKS), 0)",                              "description": "Cost Per Click. NOT a stored column — always calculate."},
            {"metric": "CPM",             "formula": "(SUM(AMOUNT_SPENT_USD) / NULLIF(SUM(IMPRESSIONS), 0)) * 1000",                "description": "Cost Per 1000 Impressions. NOT a stored column — always calculate."},
            {"metric": "TOTAL_SPEND",     "formula": "SUM(AMOUNT_SPENT_USD)",                                                       "description": "Total spend for the filtered period."},
        ],
        "relationships": [
            "SPEND_DATE → DIM_DATE.DATE_KEY",
            "CAMPAIGN_ID → DIM_CAMPAIGN.CAMPAIGN_ID",
            "AD_GROUP_ID → DIM_AD_GROUP.AD_GROUP_ID",
        ]
    },

    # ─────────────────────────────────────
    #  TABLE 7 — FACT_CONVERSIONS
    # ─────────────────────────────────────
    {
        "table": "FACT_CONVERSIONS",
        "schema": "gold",
        "description": "Conversion events attributed to ad campaigns. One row per conversion event. Use for ROAS, CPA, CVR queries.",
        "grain": "One row per CONVERSION_ID",
        "columns": [
            {"column": "CONVERSION_ID",              "type": "VARCHAR(100)",  "pk": True,  "fk": None,                              "nullable": False, "description": "Primary key. Unique conversion event ID."},
            {"column": "CONVERSION_DATE",            "type": "DATE",          "pk": False, "fk": "DIM_DATE.DATE_KEY",               "nullable": False, "description": "Date conversion occurred. FK to DIM_DATE.DATE_KEY."},
            {"column": "CAMPAIGN_ID",                "type": "VARCHAR(50)",   "pk": False, "fk": "DIM_CAMPAIGN.CAMPAIGN_ID",        "nullable": False, "description": "FK to DIM_CAMPAIGN."},
            {"column": "AD_GROUP_ID",                "type": "VARCHAR(50)",   "pk": False, "fk": "DIM_AD_GROUP.AD_GROUP_ID",        "nullable": True,  "description": "FK to DIM_AD_GROUP. NULL if not tracked at ad group level."},
            {"column": "AD_CREATIVE_ID",             "type": "VARCHAR(50)",   "pk": False, "fk": "DIM_AD_CREATIVE.AD_CREATIVE_ID",  "nullable": True,  "description": "FK to DIM_AD_CREATIVE. NULL if not tracked at creative level."},
            {"column": "PLATFORM",                   "type": "VARCHAR(50)",   "pk": False, "fk": None,                              "nullable": False, "description": "Attribution platform."},
            {"column": "USER_ID",                    "type": "VARCHAR(100)",  "pk": False, "fk": None,                              "nullable": True,  "description": "Anonymized user identifier. NULL for non-logged-in users."},
            {"column": "SESSION_ID",                 "type": "VARCHAR(100)",  "pk": False, "fk": "FACT_UTM_SESSIONS.SESSION_ID",    "nullable": True,  "description": "Web session ID at time of conversion. FK to FACT_UTM_SESSIONS."},
            {"column": "CONVERSION_TYPE",            "type": "VARCHAR(100)",  "pk": False, "fk": None,                              "nullable": False, "description": "Type of conversion. Allowed values: 'PURCHASE', 'LEAD', 'SIGN_UP', 'DOWNLOAD', 'ADD_TO_CART', 'CHECKOUT_INITIATED', 'FORM_SUBMIT', 'CALL', 'APP_INSTALL'"},
            {"column": "CONVERSION_VALUE_USD",       "type": "NUMBER(18,4)",  "pk": False, "fk": None,                              "nullable": False, "description": "Revenue value in USD. 0 for non-revenue events like LEAD, SIGN_UP. Filter WHERE CONVERSION_TYPE = 'PURCHASE' for revenue-only queries."},
            {"column": "ATTRIBUTION_MODEL",          "type": "VARCHAR(50)",   "pk": False, "fk": None,                              "nullable": False, "description": "Attribution model used. Allowed values: 'LAST_CLICK', 'FIRST_CLICK', 'LINEAR', 'TIME_DECAY', 'DATA_DRIVEN'. ALWAYS filter on this to avoid double-counting."},
            {"column": "ATTRIBUTION_WINDOW_DAYS",    "type": "NUMBER(3)",     "pk": False, "fk": None,                              "nullable": False, "description": "Attribution lookback window in days. Typical values: 7, 14, 30."},
            {"column": "CLICK_TO_CONVERSION_DAYS",   "type": "NUMBER(5)",     "pk": False, "fk": None,                              "nullable": True,  "description": "Days elapsed between ad click and this conversion event."},
            {"column": "CREATED_AT",                 "type": "TIMESTAMP_NTZ", "pk": False, "fk": None,                              "nullable": False, "description": "Row load timestamp."},
        ],
        "calculated_metrics": [
            {"metric": "CVR",             "formula": "COUNT(CONVERSION_ID) / NULLIF(SUM(clicks_from_FACT_AD_PERFORMANCE), 0)",       "description": "Conversion Rate. Requires joining FACT_AD_PERFORMANCE for clicks denominator."},
            {"metric": "CPA",             "formula": "SUM(AMOUNT_SPENT_USD from FACT_SPEND) / NULLIF(COUNT(CONVERSION_ID), 0)",      "description": "Cost Per Acquisition. Requires joining FACT_SPEND."},
            {"metric": "ROAS",            "formula": "SUM(CONVERSION_VALUE_USD) / NULLIF(SUM(AMOUNT_SPENT_USD from FACT_SPEND), 0)", "description": "Return On Ad Spend. Requires joining FACT_SPEND. NOT a stored column."},
        ],
        "relationships": [
            "CONVERSION_DATE → DIM_DATE.DATE_KEY",
            "CAMPAIGN_ID → DIM_CAMPAIGN.CAMPAIGN_ID",
            "AD_GROUP_ID → DIM_AD_GROUP.AD_GROUP_ID",
            "AD_CREATIVE_ID → DIM_AD_CREATIVE.AD_CREATIVE_ID",
            "SESSION_ID → FACT_UTM_SESSIONS.SESSION_ID",
        ]
    },

    # ─────────────────────────────────────
    #  TABLE 8 — FACT_UTM_SESSIONS
    # ─────────────────────────────────────
    {
        "table": "FACT_UTM_SESSIONS",
        "schema": "gold",
        "description": "Web sessions with UTM tracking from Google Analytics / CDP. Links ad traffic to on-site behaviour.",
        "grain": "One row per SESSION_ID",
        "columns": [
            {"column": "SESSION_ID",               "type": "VARCHAR(100)",  "pk": True,  "fk": None,                          "nullable": False, "description": "Primary key. Unique session identifier."},
            {"column": "SESSION_DATE",             "type": "DATE",          "pk": False, "fk": "DIM_DATE.DATE_KEY",           "nullable": False, "description": "Date session started. FK to DIM_DATE.DATE_KEY."},
            {"column": "USER_ID",                  "type": "VARCHAR(100)",  "pk": False, "fk": None,                          "nullable": True,  "description": "Anonymized user ID. NULL for anonymous sessions."},
            {"column": "UTM_SOURCE",               "type": "VARCHAR(255)",  "pk": False, "fk": None,                          "nullable": True,  "description": "UTM source param. Examples: 'google', 'facebook', 'linkedin', 'email', 'organic'"},
            {"column": "UTM_MEDIUM",               "type": "VARCHAR(255)",  "pk": False, "fk": None,                          "nullable": True,  "description": "UTM medium param. Examples: 'cpc', 'cpm', 'email', 'social', 'organic', 'referral'"},
            {"column": "UTM_CAMPAIGN",             "type": "VARCHAR(255)",  "pk": False, "fk": None,                          "nullable": True,  "description": "UTM campaign param — stores CAMPAIGN_NAME string, NOT CAMPAIGN_ID. Do NOT join this directly to DIM_CAMPAIGN.CAMPAIGN_ID."},
            {"column": "UTM_CONTENT",              "type": "VARCHAR(255)",  "pk": False, "fk": None,                          "nullable": True,  "description": "UTM content param (ad creative label). NULL if not set."},
            {"column": "UTM_TERM",                 "type": "VARCHAR(255)",  "pk": False, "fk": None,                          "nullable": True,  "description": "UTM keyword/term param. NULL if not set."},
            {"column": "LANDING_PAGE_URL",         "type": "VARCHAR(2000)", "pk": False, "fk": None,                          "nullable": True,  "description": "First page URL of the session."},
            {"column": "DEVICE_TYPE",              "type": "VARCHAR(20)",   "pk": False, "fk": None,                          "nullable": True,  "description": "User device. Allowed values: 'DESKTOP', 'MOBILE', 'TABLET'"},
            {"column": "BROWSER",                  "type": "VARCHAR(50)",   "pk": False, "fk": None,                          "nullable": True,  "description": "Browser name. Examples: 'Chrome', 'Safari', 'Firefox', 'Edge'"},
            {"column": "COUNTRY_CODE",             "type": "VARCHAR(2)",    "pk": False, "fk": None,                          "nullable": True,  "description": "ISO 2-letter country code. Examples: 'IN', 'US', 'GB'"},
            {"column": "CITY",                     "type": "VARCHAR(100)",  "pk": False, "fk": None,                          "nullable": True,  "description": "City name of the session user."},
            {"column": "SESSION_DURATION_SECONDS", "type": "NUMBER(10)",    "pk": False, "fk": None,                          "nullable": True,  "description": "Total session duration in seconds."},
            {"column": "PAGES_VIEWED",             "type": "NUMBER(5)",     "pk": False, "fk": None,                          "nullable": False, "description": "Number of pages viewed in this session."},
            {"column": "BOUNCED",                  "type": "BOOLEAN",       "pk": False, "fk": None,                          "nullable": False, "description": "TRUE if user left after viewing only 1 page (bounce)."},
            {"column": "CREATED_AT",               "type": "TIMESTAMP_NTZ", "pk": False, "fk": None,                          "nullable": False, "description": "Row load timestamp."},
        ],
        "relationships": [
            "SESSION_DATE → DIM_DATE.DATE_KEY",
            "SESSION_ID → FACT_CONVERSIONS.SESSION_ID",
        ]
    },
]


# ============================================================
#  BUSINESS RULES — inject this into your system prompt too
# ============================================================

business_rules = [
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
        "user_ask": "month wise click through rate",
        "sql": """
SELECT
    DATE_TRUNC('MONTH', f.EVENT_DATE)                                          AS MONTH,
    c.CAMPAIGN_NAME,
    c.PLATFORM,
    SUM(f.IMPRESSIONS)                                                         AS TOTAL_IMPRESSIONS,
    SUM(f.CLICKS)                                                              AS TOTAL_CLICKS,
    ROUND(SUM(f.CLICKS) / NULLIF(SUM(f.IMPRESSIONS), 0) * 100, 4)             AS CTR_PERCENT
FROM gold.FACT_AD_PERFORMANCE f
JOIN gold.DIM_CAMPAIGN c ON f.CAMPAIGN_ID = c.CAMPAIGN_ID
GROUP BY 1, 2, 3
ORDER BY 1 DESC, CTR_PERCENT DESC;
"""
    },
    {
        "user_ask": "month wise total spend by platform",
        "sql": """
SELECT
    DATE_TRUNC('MONTH', s.SPEND_DATE)                                          AS MONTH,
    s.PLATFORM,
    SUM(s.AMOUNT_SPENT_USD)                                                    AS TOTAL_SPEND_USD
FROM gold.FACT_SPEND s
GROUP BY 1, 2
ORDER BY 1 DESC, TOTAL_SPEND_USD DESC;
"""
    },
    {
        "user_ask": "month wise ROAS by campaign",
        "sql": """
SELECT
    DATE_TRUNC('MONTH', cv.CONVERSION_DATE)                                    AS MONTH,
    c.CAMPAIGN_NAME,
    SUM(cv.CONVERSION_VALUE_USD)                                               AS TOTAL_REVENUE_USD,
    SUM(s.AMOUNT_SPENT_USD)                                                    AS TOTAL_SPEND_USD,
    ROUND(SUM(cv.CONVERSION_VALUE_USD) / NULLIF(SUM(s.AMOUNT_SPENT_USD), 0), 4) AS ROAS
FROM gold.FACT_CONVERSIONS cv
JOIN gold.DIM_CAMPAIGN c
    ON cv.CAMPAIGN_ID = c.CAMPAIGN_ID
JOIN gold.FACT_SPEND s
    ON cv.CAMPAIGN_ID = s.CAMPAIGN_ID
    AND DATE_TRUNC('MONTH', cv.CONVERSION_DATE) = DATE_TRUNC('MONTH', s.SPEND_DATE)
WHERE cv.ATTRIBUTION_MODEL = 'LAST_CLICK'
  AND cv.CONVERSION_TYPE = 'PURCHASE'
GROUP BY 1, 2
ORDER BY 1 DESC, ROAS DESC;
"""
    },
    {
        "user_ask": "month wise CPA by campaign",
        "sql": """
SELECT
    DATE_TRUNC('MONTH', cv.CONVERSION_DATE)                                    AS MONTH,
    c.CAMPAIGN_NAME,
    COUNT(cv.CONVERSION_ID)                                                    AS TOTAL_CONVERSIONS,
    SUM(s.AMOUNT_SPENT_USD)                                                    AS TOTAL_SPEND_USD,
    ROUND(SUM(s.AMOUNT_SPENT_USD) / NULLIF(COUNT(cv.CONVERSION_ID), 0), 4)    AS CPA_USD
FROM gold.FACT_CONVERSIONS cv
JOIN gold.DIM_CAMPAIGN c
    ON cv.CAMPAIGN_ID = c.CAMPAIGN_ID
JOIN gold.FACT_SPEND s
    ON cv.CAMPAIGN_ID = s.CAMPAIGN_ID
    AND DATE_TRUNC('MONTH', cv.CONVERSION_DATE) = DATE_TRUNC('MONTH', s.SPEND_DATE)
WHERE cv.ATTRIBUTION_MODEL = 'LAST_CLICK'
GROUP BY 1, 2
ORDER BY 1 DESC;
"""
    },
    {
        "user_ask": "top performing ad creatives by CTR",
        "sql": """
SELECT
    cr.AD_NAME,
    cr.AD_FORMAT,
    cr.CALL_TO_ACTION,
    SUM(f.IMPRESSIONS)                                                         AS TOTAL_IMPRESSIONS,
    SUM(f.CLICKS)                                                              AS TOTAL_CLICKS,
    ROUND(SUM(f.CLICKS) / NULLIF(SUM(f.IMPRESSIONS), 0) * 100, 4)             AS CTR_PERCENT
FROM gold.FACT_AD_PERFORMANCE f
JOIN gold.DIM_AD_CREATIVE cr ON f.AD_CREATIVE_ID = cr.AD_CREATIVE_ID
WHERE f.IMPRESSIONS > 1000
GROUP BY 1, 2, 3
ORDER BY CTR_PERCENT DESC
LIMIT 20;
"""
    },
    {
        "user_ask": "month wise conversions by conversion type",
        "sql": """
SELECT
    DATE_TRUNC('MONTH', cv.CONVERSION_DATE)                                    AS MONTH,
    cv.CONVERSION_TYPE,
    COUNT(cv.CONVERSION_ID)                                                    AS TOTAL_CONVERSIONS,
    SUM(cv.CONVERSION_VALUE_USD)                                               AS TOTAL_VALUE_USD
FROM gold.FACT_CONVERSIONS cv
WHERE cv.ATTRIBUTION_MODEL = 'LAST_CLICK'
GROUP BY 1, 2
ORDER BY 1 DESC, TOTAL_CONVERSIONS DESC;
"""
    },
]


def build_system_prompt(data_dict, business_rules, query_patterns):
    prompt = "You are a Snowflake SQL expert for a marketing analytics data warehouse.\n\n"
    prompt += "## STRICT RULES\n"
    for i, rule in enumerate(business_rules, 1):
        prompt += f"{i}. {rule}\n"

    prompt += "\n## DATA DICTIONARY\n"
    for table in data_dict:
        prompt += f"\n### TABLE: {table['schema']}.{table['table']}\n"
        prompt += f"Description: {table['description']}\n"
        prompt += f"Grain: {table['grain']}\n"
        prompt += "Columns:\n"
        for col in table["columns"]:
            fk_note = f" | FK → {col['fk']}" if col["fk"] else ""
            null_note = " | NULLABLE" if col["nullable"] else " | NOT NULL"
            prompt += f"  - {col['column']} ({col['type']}){fk_note}{null_note}: {col['description']}\n"
        if "calculated_metrics" in table:
            prompt += "Calculated Metrics (NOT stored columns):\n"
            for m in table["calculated_metrics"]:
                prompt += f"  - {m['metric']} = {m['formula']}  → {m['description']}\n"

    prompt += "\n## EXAMPLE QUERY PATTERNS\n"
    for qp in query_patterns:
        prompt += f"\nUser asks: \"{qp['user_ask']}\"\nSQL:\n{qp['sql']}\n"

    return prompt