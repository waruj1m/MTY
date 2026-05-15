from rich.style import Style

RAW_WORDS = """the be to of and a in that have it for not on with he as you do at this but his by from they we say her she or an will my one all would there their what so up out if about who get which go me when make can like time no just him know take people into year your good some could them see other than then now look only come its over think also back after use two how our work first well even new want because any these give day most us great between need yet place small under before why quick brown fox jumps lazy dog right long live where after big house world life hand part child eye woman head stand own page should found study still learn around form food water run end along group young turn were away here thing home many ask man move try last point city tree cross country week church party program social machine change line care question large different number short system public write course long""".split()
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
