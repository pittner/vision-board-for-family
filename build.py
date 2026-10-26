#!/usr/bin/env python3
"""Builds index.html for pittner/vision-board-for-family.

A single-purpose page for the seasonal "family vision board" / "family goals 2027" intent
(families plan the new year together over the winter holidays): 36 family goals in 6 groups, each
with why it matters and a first step the whole family can do this week, and a link that opens the
free maker with that goal and step already filled in (?goal=&step=&layout=text&mode=wallpaper, T-098),
so it can go on a parent's phone or be printed for the fridge. Plus 12 questions kids can answer,
a 45-minute family plan, a box for your own family goal, and FAQ.

No dependencies. Run: python3 build.py
"""
import html as _html
import json
import pathlib
from urllib.parse import urlencode

HERE = pathlib.Path(__file__).resolve().parent
URL = "https://pittner.github.io/vision-board-for-family/"
SRC = "ghpages_family"
CAMPAIGN = "family_2027"

# (group, [(family goal, why it matters, a first step the family does this week)])
GROUPS = [
    ("Time together", [
        ("A family night every week", "Kids remember the evenings, not the gifts.", "Pick the night and let the youngest choose the first game"),
        ("Dinner at the table, phones away", "Dinner is the one meeting the whole family has every day.", "Put a phone basket by the table tonight"),
        ("One adventure every month", "Twelve small adventures make a big year.", "Write 12 ideas on paper and pull the first one out of a hat"),
        ("A Sunday breakfast we cook together", "Cooking together is a lesson and a party at once.", "Choose this Sunday's menu with the kids"),
        ("Screen-free Saturday mornings", "Boredom is where kids start inventing.", "Agree on the hours and plan one thing to do instead"),
        ("Read together every evening", "Ten minutes of a story is the calmest part of the day.", "Pick a family book and read the first chapter tonight"),
    ]),
    ("Home", [
        ("A calm morning routine", "Fewer rushed mornings, fewer tears before school.", "Pack bags and lay out clothes the evening before, three nights in a row"),
        ("Everyone helps at home", "Kids who help feel they belong.", "Give each child one job that is theirs this week"),
        ("A tidy-up song, ten minutes a day", "Short and daily beats a big Saturday fight.", "Choose the song and do the first ten-minute tidy tonight"),
        ("A cosy corner just for reading", "A place invites the habit.", "Pick the corner and move one lamp and one cushion there"),
        ("Less stuff, more space to play", "Fewer toys get played with more.", "Each child picks five toys to give away this weekend"),
        ("A family calendar on the wall", "When everyone can see the week, fewer things are forgotten.", "Hang a paper calendar and fill in next week together"),
    ]),
    ("Health and outdoors", [
        ("Outside every day, whatever the weather", "Fresh air helps sleep, mood and appetite.", "Plan one walk after school or dinner this week"),
        ("Bedtime on time", "Rested kids and rested parents are kinder to each other.", "Agree on bedtimes and try them for three nights"),
        ("Cook one new healthy dish a week", "Kids eat what they helped make.", "Let each child pick one vegetable at the shop"),
        ("Learn to ride, swim or skate", "A new skill gives a child a proud year.", "Pick the skill and find the first lesson or park"),
        ("A family hike or race in 2027", "A shared finish line is a story you retell for years.", "Choose one event and put the date in the calendar"),
        ("Move together on the weekend", "Exercise is easier as a game.", "Plan one bike ride, swim or football match this weekend"),
    ]),
    ("Learning and growing", [
        ("Every child learns one new thing", "Kids grow when they choose what to learn.", "Ask each child what they want to learn and write it down"),
        ("A library trip every two weeks", "Free books and a small ritual in one.", "Get library cards for everyone this week"),
        ("Homework without the fight", "A fixed time and place ends most arguments.", "Agree on homework time and set up one quiet spot"),
        ("Learn a little of a new language", "Saying hello in another language makes travel more fun.", "Learn five words together at dinner this week"),
        ("Try a new hobby as a family", "Being beginners together is good for everyone.", "Each person suggests one hobby, try one this month"),
        ("Money lessons for kids", "Saving for something real teaches more than any talk.", "Give each child a jar and name what they save for"),
    ]),
    ("Travel and memories", [
        ("One family trip in 2027", "Trips are where the best family stories start.", "Pick the month and each person names one wish for it"),
        ("Visit grandparents more often", "Time with grandparents is a gift for both sides.", "Put the next visit in the calendar today"),
        ("A photo book of our year", "Photos on paper get looked at, photos in the cloud do not.", "Make a folder and save the first five photos of the month"),
        ("Camp under the stars once", "Kids never forget the first night in a tent.", "Find one campsite within two hours of home"),
        ("A new place close to home each season", "Adventure does not need a plane.", "Write four places, one per season, and choose the first"),
        ("A family time capsule", "Opening it next December is a tradition in itself.", "Each person writes one wish for 2027 and seals it in a box"),
    ]),
    ("Kindness and traditions", [
        ("Our own family traditions", "Rituals tell kids who we are as a family.", "Choose one new tradition to start this December"),
        ("Say one thing we are thankful for at dinner", "Gratitude said out loud changes the mood of a table.", "Start tonight, the youngest goes first"),
        ("Help someone together every season", "Giving as a family teaches more than talking about it.", "Choose one cause and plan one afternoon for it"),
        ("Fewer shouts, more hugs", "Kids copy how we handle hard moments.", "Agree on a family calm-down word and practise it once"),
        ("Celebrate small wins", "Noticing effort helps kids keep trying.", "Put a 'win of the week' note on the fridge this Friday"),
        ("A monthly family meeting", "Kids who are asked feel heard.", "Set a reminder for the last Sunday of the month"),
    ]),
]

QUESTIONS = [
    "What was your favorite day with our family in 2026?",
    "What made you really proud of yourself this year?",
    "What do you want to learn or get better at next year?",
    "Where would you love to go together in 2027?",
    "What is one thing we should do more often as a family?",
    "What is one thing we should do less often?",
    "What does a perfect family Saturday look like for you?",
    "Which family tradition do you never want to stop?",
    "What new tradition should we start?",
    "Who would you like to see more often?",
    "How can we help each other when someone has a bad day?",
    "What is one wish you have for our family next year?",
]

PLAN = [
    ("10 minutes: look back.", "Everyone, youngest first, names a favorite moment of 2026. Parents only listen and write."),
    ("15 minutes: ask the questions.", "Go around the table with the 12 questions below. Little kids can draw their answer instead of saying it."),
    ("10 minutes: pick three family goals.", "One for time together, one for home or health, one just for fun. Let the kids pick at least one of them."),
    ("10 minutes: make it visible.", "Turn your favorite goal and its first step into a phone lock screen, print it for the fridge, or make a full board together."),
]

FAQ = [
    ("What is a family vision board?",
     "A board of the goals your family shares for the coming year, such as more time together, a trip, a calmer home or a new skill. "
     "You make it together with your kids, so it doubles as a conversation about what everyone wants."),
    ("How do you make a family vision board with kids?",
     "Look back at the year together, ask each child a few simple questions, pick three family goals and make them visible. "
     "This page has 36 family goals with a first step, 12 questions kids can answer and a 45-minute plan."),
    ("What should a family put on a vision board?",
     "Goals the whole family cares about: time together, home, health and outdoors, learning, travel and kindness. "
     "Add one first step to each goal so the board says what to do this week, not only what to dream about."),
    ("What age is a family vision board for?",
     "From about four years up. Younger kids draw or pick pictures, older kids write their own goals and choose the first steps."),
    ("Is the maker free?",
     "Yes. It runs in your browser, needs no account and uploads nothing. Save the image to a phone or print it for the fridge."),
    ("Can we make a full vision board with several goals?",
     "Yes. Start from your family goal in the AI vision board generator: you see a free preview, and unlocking the full-size board is optional (8.99 EUR)."),
]

def e(s):
    return _html.escape(s, quote=True)


def link(path, **extra):
    q = dict(extra)
    q.update({"utm_source": SRC, "utm_medium": "referral", "utm_campaign": CAMPAIGN})
    return "https://visionboard.bemooore.com" + path + "?" + urlencode(q)


def maker(goal, step, content):
    return link("/free-vision-board-maker/", goal=goal, step=step, layout="text", mode="wallpaper", utm_content=content)


TOOL = link("/free-vision-board-maker/", mode="wallpaper", layout="text", utm_content="plan_tool")
AI = link("/en/create.php", utm_content="faq_ai")
AI_PLAN = link("/en/create.php", utm_content="plan_ai")
HOME = link("/", utm_content="footer_home")


def slug(s):
    return "-".join("".join(c if c.isalnum() else " " for c in s.lower()).split())


def build():
    count = sum(len(gs) for _, gs in GROUPS)
    nav = " ".join(f'<a class="chip" href="#{slug(g)}">{e(g)}</a>' for g, _ in GROUPS)
    blocks = []
    for g, goals in GROUPS:
        cards = []
        for i, (goal, why, step) in enumerate(goals, 1):
            cid = f"{slug(g)}_{i}"
            cards.append(
                f'      <div class="wcard" id="g-{cid}"><h3>{e(goal)}</h3><p>{e(why)}</p>'
                f'<p class="step"><span>First step this week:</span> {e(step)}</p>'
                f'<a class="btn" href="{e(maker(goal, step, "goal_" + cid))}" data-cta="goal_{cid}">Make it our family screen</a></div>')
        blocks.append(f'  <section class="grp" id="{slug(g)}">\n    <h2>{e(g)}</h2>\n    <div class="grid">\n'
                      + "\n".join(cards) + "\n    </div>\n  </section>")
    questions = "\n".join(f"    <li>{e(q)}</li>" for q in QUESTIONS)
    plan = "\n".join(f"    <li><b>{e(a)}</b> {e(b)}</li>" for a, b in PLAN)
    faq_html = "\n".join(f"  <h3>{e(q)}</h3>\n  <p>{e(a)}</p>" for q, a in FAQ)
    ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        ensure_ascii=False)
    page = TEMPLATE
    for k, v in {
        "%%NAV%%": nav, "%%GROUPS%%": "\n\n".join(blocks), "%%QUESTIONS%%": questions, "%%PLAN%%": plan,
        "%%FAQ%%": faq_html, "%%LD%%": ld, "%%COUNT%%": str(count), "%%NQ%%": str(len(QUESTIONS)),
        "%%TOOL%%": e(TOOL), "%%AI%%": e(AI), "%%AIPLAN%%": e(AI_PLAN), "%%HOME%%": e(HOME),
        "%%URL%%": URL, "%%SRC%%": SRC, "%%CAMPAIGN%%": CAMPAIGN,
    }.items():
        page = page.replace(k, v)
    (HERE / "index.html").write_text(page, encoding="utf-8")
    print("index.html", len(page.encode()), "bytes,", count, "goals")


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Family Vision Board 2027: %%COUNT%% Family Goals, %%NQ%% Questions for Kids &amp; a Free Maker</title>
<meta name="description" content="Plan 2027 as a family: %%COUNT%% family goals, each with a first step for this week, %%NQ%% questions kids can answer and a 45-minute plan. Turn your goal into a free lock screen or a page for the fridge. No signup.">
<link rel="canonical" href="%%URL%%">
<meta property="og:type" content="website">
<meta property="og:title" content="Family vision board 2027 - %%COUNT%% family goals and a free maker">
<meta property="og:description" content="Family goals with a first step, %%NQ%% questions for kids, and a lock screen or fridge page in one click. Free, no signup.">
<meta property="og:url" content="%%URL%%">
<style>
:root{--ink:#111827;--muted:#6B7280;--rule:#E5E7EB;--acc:#0F766E;--bg:#F8FBFA}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
a{color:var(--acc)}
.wrap{max-width:1000px;margin:0 auto;padding:0 20px}
header.hero{padding:48px 0 18px}
h1{font:600 clamp(28px,4.4vw,42px)/1.15 Georgia,"Times New Roman",serif;margin:0 0 14px;letter-spacing:-.01em}
.lede{font-size:18px;color:#374151;max-width:64ch;margin:0 0 14px}
.meta{font-size:14px;color:var(--muted);margin:0}
.btn{appearance:none;display:inline-block;text-decoration:none;border:1px solid #D1D5DB;background:#fff;color:var(--ink);padding:9px 15px;border-radius:999px;font:500 14px/1 inherit;cursor:pointer}
.btn:hover{border-color:var(--acc);color:var(--acc)}
.btn.primary{background:var(--acc);border-color:var(--acc);color:#fff}
.btn.primary:hover{background:#115E59;color:#fff}
.own{background:#fff;border:1px solid var(--rule);border-radius:16px;padding:18px;margin:8px 0 22px}
.own h2{font:600 21px/1.3 Georgia,serif;margin:0 0 10px}
.own .row{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1.3fr) auto;gap:8px;align-items:end}
@media (max-width:760px){.own .row{grid-template-columns:1fr}}
.own label{display:block;font-size:13px;color:var(--muted);margin:0 0 4px}
.own input{width:100%;border:1px solid #D1D5DB;border-radius:10px;padding:10px 12px;font:16px/1.3 inherit;background:#fff}
.own input:focus{outline:2px solid var(--acc);outline-offset:1px;border-color:var(--acc)}
#ownMsg{font-size:13px;color:var(--muted);margin:8px 0 0}
.chips{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 6px}
.chip{display:inline-block;text-decoration:none;border:1px solid var(--rule);background:#fff;color:#374151;padding:6px 12px;border-radius:999px;font-size:14px}
.chip:hover{border-color:var(--acc);color:var(--acc)}
section.grp{padding:22px 0 8px}
section.grp h2{font:600 24px/1.25 Georgia,serif;margin:0 0 12px}
.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
@media (max-width:860px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:520px){.grid{grid-template-columns:1fr}}
.wcard{background:#fff;border:1px solid var(--rule);border-radius:14px;padding:14px 14px 16px;display:flex;flex-direction:column}
.wcard h3{font:600 19px/1.25 Georgia,serif;margin:0 0 6px}
.wcard p{margin:0 0 8px;color:#374151;font-size:15px}
.wcard .step{font-size:14px;color:var(--muted);flex:1}
.wcard .step span{color:var(--acc);font-weight:600}
.wcard .btn{align-self:flex-start}
section.block{padding:30px 0;border-top:1px solid var(--rule);margin-top:20px}
section.block h2{font:600 24px/1.25 Georgia,serif;margin:0 0 8px}
section.block>p{max-width:70ch;color:#374151}
ol.how,ol.qs{max-width:70ch;color:#374151;padding-left:22px}
ol.how li,ol.qs li{margin:0 0 10px}
.faq h3{font:600 16px/1.4 inherit;margin:18px 0 4px}
.faq p{margin:0;color:#374151;max-width:70ch}
footer{padding:28px 0 60px;font-size:14px;color:var(--muted);border-top:1px solid var(--rule)}
</style>
</head>
<body>
<div class="wrap">
<header class="hero">
  <h1>Family vision board 2027: %%COUNT%% family goals, made together with your kids</h1>
  <p class="lede">The winter holidays are the one time the whole family sits at the same table with no rush. Use one evening to plan 2027 together. Below are %%COUNT%% family goals, each with why it matters and a first step the whole family can do this week, plus %%NQ%% questions even young kids can answer. Press a goal and it opens in a free maker with the first step under it: save it as a lock screen or print it for the fridge. No signup, nothing uploaded.</p>
  <p class="meta">%%COUNT%% goals in 6 groups &middot; %%NQ%% questions for kids &middot; 45-minute plan &middot; lock screen or fridge page &middot; free, MIT licensed</p>
</header>

<div class="own" id="own">
  <h2>Already know your family goal?</h2>
  <div class="row">
    <div><label for="ownGoal">Our family goal for 2027</label><input id="ownGoal" maxlength="120" placeholder="e.g. One adventure every month" autocomplete="off"></div>
    <div><label for="ownStep">Our first step (optional)</label><input id="ownStep" maxlength="120" placeholder="e.g. Pull the first idea out of a hat on Sunday" autocomplete="off"></div>
    <button class="btn primary" id="ownGo" type="button">Make it our family screen</button>
  </div>
  <p id="ownMsg">Opens the free maker with your goal filled in. Change colors or layout there, then save it to a phone or print it for the fridge.</p>
</div>

<nav class="chips" aria-label="Groups">%%NAV%% <a class="chip" href="#questions">%%NQ%% questions for kids</a> <a class="chip" href="#plan">45-minute plan</a></nav>

%%GROUPS%%

<section class="block" id="questions">
  <h2>%%NQ%% questions to ask your kids before you choose</h2>
  <p>Go around the table, youngest first. Parents answer too. Write down every answer that makes the others nod: those are your family goals.</p>
  <ol class="qs">
%%QUESTIONS%%
  </ol>
</section>

<section class="block" id="plan">
  <h2>Make it as a family in 45 minutes</h2>
  <ol class="how">
%%PLAN%%
  </ol>
  <p><a class="btn primary" href="%%TOOL%%" data-cta="plan_tool">Open the free lock-screen maker</a>
     <a class="btn" href="%%AIPLAN%%" data-cta="plan_ai">Make a full board with several goals</a></p>
</section>

<section class="block faq">
  <h2>Questions</h2>
%%FAQ%%
  <p style="margin-top:16px"><a class="btn" href="%%AI%%" data-cta="faq_ai">Make a full vision board around our family goals</a></p>
</section>

<footer>
  MIT licensed &middot; published by the team behind
  <a href="%%HOME%%" data-cta="footer_home">visionboard.bemooore.com</a> &middot;
  more: <a href="https://pittner.github.io/vision-board-for-couples/">vision board for couples</a>,
  <a href="https://pittner.github.io/vision-board-for-students/">vision board for students</a>,
  <a href="https://pittner.github.io/vision-board-party-kit/">vision board party kit</a>,
  <a href="https://pittner.github.io/word-of-the-year-2027/">word of the year 2027</a>,
  <a href="https://pittner.github.io/2027-vision-board-template/">printable 2027 vision board template</a>,
  <a href="https://pittner.github.io/vision-board-prompts/">54 vision board prompts</a>,
  <a href="https://pittner.github.io/">all free tools</a> &middot;
  <a href="https://github.com/pittner/vision-board-for-family">source</a>
</footer>
</div>

<script type="application/ld+json">
%%LD%%
</script>

<script>
(function(){
  var EP='https://visionboard.bemooore.com/api/event.php',P='%%SRC%%',engaged=false;
  function beacon(ev,label){
    try{
      var b=JSON.stringify({event:ev,utm:P+' | '+label+' | '+location.search});
      if(navigator.sendBeacon){navigator.sendBeacon(EP,new Blob([b],{type:'text/plain'}));}
      else{fetch(EP,{method:'POST',body:b,keepalive:true,mode:'no-cors'});}
    }catch(e){}
  }
  // Every link to our site carries where the visitor came from (e.g. chatgpt.com).
  var src=(location.search.match(/[?&]utm_source=([^&]+)/)||[])[1]||(document.referrer?document.referrer.split('/')[2]:'direct');
  Array.prototype.forEach.call(document.querySelectorAll('a[data-cta][href*="visionboard.bemooore.com"]'),function(a){
    a.href+='&utm_term='+encodeURIComponent('via_'+src);
  });
  function engage(how){ if(engaged)return; engaged=true; beacon('page_engaged',how); }
  setTimeout(function(){engage('dwell6s');},6000);
  window.addEventListener('scroll',function(){
    var h=document.documentElement;
    if((h.scrollTop||document.body.scrollTop)/((h.scrollHeight-h.clientHeight)||1)>0.25) engage('scroll25');
  },{passive:true});
  document.addEventListener('click',function(e){
    var a=e.target.closest('[data-cta]'); if(a) beacon('cta_click',a.getAttribute('data-cta'));
  });

  // Own family goal: same prefill as the goal cards (?goal=&step=&layout=text&mode=wallpaper).
  var g=document.getElementById('ownGoal'),s=document.getElementById('ownStep'),msg=document.getElementById('ownMsg');
  function go(){
    var goal=g.value.trim(),step=s.value.trim();
    if(!goal){ msg.textContent='Type your family goal first.'; g.focus(); return; }
    var q=new URLSearchParams({goal:goal,layout:'text',mode:'wallpaper',utm_source:P,utm_medium:'referral',
      utm_campaign:'%%CAMPAIGN%%',utm_content:'own_goal',utm_term:'via_'+src});
    if(step) q.set('step',step);
    beacon('cta_click','own_goal');
    location.href='https://visionboard.bemooore.com/free-vision-board-maker/?'+q.toString();
  }
  document.getElementById('ownGo').addEventListener('click',go);
  [g,s].forEach(function(el){ el.addEventListener('keydown',function(e){ if(e.key==='Enter') go(); }); });
})();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    build()
