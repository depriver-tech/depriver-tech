from textwrap import dedent

def lesson(title, goal, concept, code, explain, task, cases, hint, solution, answer, pitfall, extension):
    return dict(title=title, goal=goal, concept=concept, code=dedent(code).strip(), explain=explain,
                task=task, cases=cases, hint=hint, solution=dedent(solution).strip(), answer=answer,
                pitfall=pitfall, extension=extension)
