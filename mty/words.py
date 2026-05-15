from rich.style import Style

RAW_WORDS = """
the be of and a to in he have it that for they with as not on she at by
this we you do but from or which one would all will there say who make when
can more if no man out other so what time up go about than into could state
only new year some take come these know see use get like then first any work
now may such give over think most even find day also after way many must look
before great back through long where much should well people down own just
because good each those feel seem how high too place little world very still
hand old life tell write become here show house both between need mean call
under last right move thing general school never same another begin while
number part turn real leave might want point form off child few small since
against ask late home large person end open public follow during present
without again hold around possible head consider word program problem lead
system set order eye plan run keep face fact group play stand increase early
course change help line city put close case force meet once water war build
hear light unite live every country bring center let side try provide name
certain power pay result question study woman member until far night always
service away report something company week church start social room figure
nature though young less enough almost read include nothing yet better big
boy cost business value second why clear expect family complete act sense
mind experience art next near direct car law industry important girl god
several matter rather often kind among white reason action return foot care
simple within love human along appear doctor believe speak active student
month drive best door hope example body ever least understand reach effect
different idea whole control field pass fall note special talk today walk
teach low hour type carry rate remain full street easy although record sit
level local sure receive moment spirit train college music grow free cause
serve age book board recent sound office cut step class true history above
strong friend court deal support party whether either land material happen
education death agree arm mother across quite town past view society manage
answer break half fire lose money stop already effort wait able learn voice
air together cover common subject draw short wife road letter color behind
produce send term total rise century success minute remember purpose test
fight watch ago stage father table rest market prepare explain offer plant
charge ground west picture hard front modern dark surface rule future wall
farm claim firm further pressure property morning amount top outside piece
trade fear quick brown fox jumps lazy dog
""".split()

# Dedupe while preserving order so the pool stays varied and shuffle-friendly.
WORDS = list(dict.fromkeys(RAW_WORDS))

CHAR_CORRECT = Style(color="#e2b714", bold=True)
CHAR_INCORRECT = Style(color="#ca4754", bold=True)
CHAR_EXTRA = Style(color="#ca4754", bold=True, strike=True)
CHAR_CURRENT = Style(color="#d1d0c5", bold=True, underline=True)
CHAR_UNTYPED = Style(color="#646669")
CHAR_CURRENT_SPACE = Style(color="#2c2e31", bgcolor="#d1d0c5")
STYLE_BG = "#2c2e31"
STYLE_TEXT = "#d1d0c5"

TIME_OPTIONS = [15, 30, 60, 120]
WORD_OPTIONS = [10, 25, 50, 100]
