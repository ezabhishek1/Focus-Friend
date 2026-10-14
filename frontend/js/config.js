/**
 * Focus Friend - Frontend Configuration & Constants
 * Dynamically resolves API routes with sensible defaults.
 */

export const CONFIG = {
  APP_NAME: "Focus Friend",
  VERSION: "1.0.0",
  // Relative API path works regardless of host, port, or reverse proxy
  API_BASE_URL: "/api/v1",
  TIMEOUT_MS: 15000,
  HEALTH_CHECK_INTERVAL_MS: 30000,
  DEFAULT_MODEL: "phi3:mini",
  STORAGE_KEYS: {
    THEME: "focus_friend_theme",
    SFX: "focus_friend_sfx",
  },
  // Default static presets as fallback in pure offline static file scenarios
  DEFAULT_PRESETS: [
    {
      id: "manager_email",
      title: "Rambling Boss Email",
      category: "Email",
      emoji: "👔",
      text: "Hey Alex, hope your week is wrapping up nicely! I wanted to touch base regarding the Q3 product retrospective slide deck we chatted about in passing last Tuesday. Overall the executive leadership loved the initial high-level vision, but Sarah raised a few concerns about the customer churn numbers in section 4. No need to rewrite everything—it looks super promising! Could you just review the updated deck I dropped in Google Drive, fix the slide 7 metric, and send me a 2-sentence confirmation before end of day Friday so I can sign off on it? Thanks so much for all your hard work on this!"
    },
    {
      id: "slack_thread",
      title: "15-Person Slack Storm",
      category: "Slack",
      emoji: "💬",
      text: "@here hey everyone, quick heads up on the staging deployment. @marcus pushed the auth fix but @dave thinks the token refresh might still be failing for European timezones. @alex can you jump on staging and verify whether the user login session persists after 15 minutes? We need to freeze this before tomorrow's 10:00 AM sprint demo. Also reminder to submit your team lunch preferences in the poll above by noon today. Don't worry about the logging errors in Datadog, those are unrelated."
    },
    {
      id: "client_scope",
      title: "Scope-Creep Client Request",
      category: "Client",
      emoji: "📑",
      text: "Hi team, we were playing around with the latest beta build over the weekend and we really like the new dark mode! However, our marketing VP was wondering if we could quickly add support for multi-currency invoicing and automatic PDF generation before we officially go live on November 1st? I know we didn't include this in the original sprint statement of work, but it should only take a couple of lines of code right? Please let us know if this is doable or if we should set up a 45-minute sync call tomorrow at 2 PM to negotiate the deliverables."
    },
    {
      id: "discord_ping",
      title: "11:30 PM Panic Discord Ping",
      category: "Discord",
      emoji: "🚨",
      text: "@Alex hey bro sorry for pinging you so late (11:30 PM) but the client demo server just threw a 502 Bad Gateway error on the checkout endpoint. I tried restarting nginx but it looks like the postgres connection pool is exhausted. Can you log into the AWS EC2 box whenever you wake up tomorrow morning (ideally before 9 AM EST) and bounce the docker container? If not let me know so I can ping Jordan."
    }
  ]
};
