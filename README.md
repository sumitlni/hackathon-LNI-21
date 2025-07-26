# The awesome retention platform by Loud Noise Inc

Protect your employees from being poached! Use Agents!

## What this project does

It simulates a small AI company that has employees that could be poached by a large AI powerhouse. Bright Data monitors
the job postings from <Name Company Here at your peril>, and asks Senso to check if any of the current employees match
the profile. If they do, a heartfelt message is put together and sent in video format by Minimax.

## System Setup

Set up Q Developer on a Linux AMI (or locally). Then, create an mcp.json file in ~/.aws/amazonq directory. You can 
configure AWS-provided MCP Servers here, but they are not required for the demo.

Configure the following MCP Servers:
- [Senso](https://docs.senso.ai/mcp2)
- [Bright Data](https://docs.brightdata.com/api-reference/MCP-Server#self-hosted-mcp) 
- [Minimax](https://github.com/MiniMax-AI/MiniMax-MCP)

Senso requires a local installation and a bit more configuration, since it needs to run server.py locally.

## Initialization

Run
```
q chat
```
After the MCP servers are initialized, this is how the ```/tools``` output will look like:
```
Tool                                                      Permission
▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔Built-in:
- execute_bash                                            * trust read-only commands
- fs_read                                                 * trusted
- fs_write                                                * not trusted
- report_issue                                            * trusted
- use_aws                                                 * trust read-only commands

bright_data (MCP):
- bright_data___extract                                   * not trusted
- bright_data___scrape_as_html                            * not trusted
- bright_data___scrape_as_markdown                        * not trusted
- bright_data___scraping_browser_click                    * not trusted
- bright_data___scraping_browser_get_html                 * not trusted
- bright_data___scraping_browser_get_text                 * not trusted
- bright_data___scraping_browser_go_back                  * not trusted
- bright_data___scraping_browser_go_forward               * not trusted
- bright_data___scraping_browser_links                    * not trusted
- bright_data___scraping_browser_navigate                 * not trusted
- bright_data___scraping_browser_screenshot               * not trusted
- bright_data___scraping_browser_scroll                   * not trusted
- bright_data___scraping_browser_scroll_to                * not trusted
- bright_data___scraping_browser_type                     * not trusted
- bright_data___scraping_browser_wait_for                 * not trusted
- bright_data___search_engine                             * not trusted
- bright_data___session_stats                             * not trusted
- bright_data___web_data_amazon_product                   * not trusted
- bright_data___web_data_amazon_product_reviews           * not trusted
- bright_data___web_data_amazon_product_search            * not trusted
- bright_data___web_data_apple_app_store                  * not trusted
- bright_data___web_data_bestbuy_products                 * not trusted
- bright_data___web_data_booking_hotel_listings           * not trusted
- bright_data___web_data_crunchbase_company               * not trusted
- bright_data___web_data_ebay_product                     * not trusted
- bright_data___web_data_etsy_products                    * not trusted
- bright_data___web_data_facebook_company_reviews         * not trusted
- bright_data___web_data_facebook_events                  * not trusted
- bright_data___web_data_facebook_marketplace_listings    * not trusted
- bright_data___web_data_facebook_posts                   * not trusted
- bright_data___web_data_github_repository_file           * not trusted
- bright_data___web_data_google_maps_reviews              * not trusted
- bright_data___web_data_google_play_store                * not trusted
- bright_data___web_data_google_shopping                  * not trusted
- bright_data___web_data_homedepot_products               * not trusted
- bright_data___web_data_instagram_comments               * not trusted
- bright_data___web_data_instagram_posts                  * not trusted
- bright_data___web_data_instagram_profiles               * not trusted
- bright_data___web_data_instagram_reels                  * not trusted
- bright_data___web_data_linkedin_company_profile         * not trusted
- bright_data___web_data_linkedin_job_listings            * not trusted
- bright_data___web_data_linkedin_people_search           * not trusted
- bright_data___web_data_linkedin_person_profile          * not trusted
- bright_data___web_data_linkedin_posts                   * not trusted
- bright_data___web_data_reddit_posts                     * not trusted
- bright_data___web_data_reuter_news                      * not trusted
- bright_data___web_data_tiktok_comments                  * not trusted
- bright_data___web_data_tiktok_posts                     * not trusted
- bright_data___web_data_tiktok_profiles                  * not trusted
- bright_data___web_data_tiktok_shop                      * not trusted
- bright_data___web_data_walmart_product                  * not trusted
- bright_data___web_data_walmart_seller                   * not trusted
- bright_data___web_data_x_posts                          * not trusted
- bright_data___web_data_yahoo_finance_business           * not trusted
- bright_data___web_data_youtube_comments                 * not trusted
- bright_data___web_data_youtube_profiles                 * not trusted
- bright_data___web_data_youtube_videos                   * not trusted
- bright_data___web_data_zara_products                    * not trusted
- bright_data___web_data_zillow_properties_listing        * not trusted
- bright_data___web_data_zoominfo_company_profile         * not trusted

mini_max (MCP):
- mini_max___generate_video                               * not trusted
- mini_max___list_voices                                  * not trusted
- mini_max___music_generation                             * not trusted
- mini_max___play_audio                                   * not trusted
- mini_max___query_video_generation                       * not trusted
- mini_max___text_to_audio                                * not trusted
- mini_max___text_to_image                                * not trusted
- mini_max___voice_clone                                  * not trusted
- mini_max___voice_design                                 * not trusted

senso (MCP):
- senso___add_raw_content                                 * not trusted
- senso___create_prompt                                   * not trusted
- senso___create_template                                 * not trusted
- senso___generate_content                                * not trusted
- senso___generate_with_prompt                            * not trusted
- senso___list_prompts                                    * not trusted
- senso___list_templates                                  * not trusted
- senso___search_content                                  * not trusted
- senso___update_prompt                                   * not trusted
- senso___update_template                                 * not trusted

```

The steps are:
1. Use ```senso___add_raw_content``` to add dummy employee entries. In real world, this would access the HR systems.
2. Use ```bright_data___web_data_linkedin_job_listings``` to find out the latest job listings, and find out which roles are in active demand.
3. Use ```senso___search_content``` to find the employees at risk of being poached. The model being used, Claude Sonnet 3.5, understands what we are trying to do and sets up the prompts automatically.
4. Finally, use ```mini_max___generate_video``` to generate a heartfelt video saying "Please don't go!". The original plan was to throw $$$ in the air, but that is somehow not allowed by the AI.


