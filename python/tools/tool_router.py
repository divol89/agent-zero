# tool_router.py

# from agent import Agent  # Asegúrate de tener una clase Agent definida en agent.py


# class ToolRouter:
#     def __init__(self, agent):
#         self.agent = agent
#         self.tools = {
#             "code_execution_tool": agent.tools.get("code_execution_tool"),
#             "webpage_content_tool": agent.tools.get("webpage_content_tool")
#         }

#     async def execute(self, task, **kwargs):
#         # Check the context of the task
#         if self.is_web_interaction(task):
#             # Pasar los argumentos al webpage_content_tool
#             return await self.tools["webpage_content_tool"].execute(**kwargs)
#         elif self.is_code_execution(task):
#             # Pasar los argumentos al code_execution_tool
#             return await self.tools["code_execution_tool"].execute(**kwargs)
#         else:
#             return Response(message="Error: No suitable tool found for this task.", break_loop=True)

#     def is_web_interaction(self, task):
#         # Keywords that imply a web browser action
#         web_actions = ["click", "type", "search", "navigate", "scroll", "accept terms"]
#         return any(action in task.lower() for action in web_actions)

#     def is_code_execution(self, task):
#         # Keywords that imply a code execution or terminal interaction
#         code_actions = ["install", "run", "execute", "shell", "command", "terminal"]
#         return any(action in task.lower() for action in code_actions)


# class ToolRouter:
#     def __init__(self, agent):
#         self.agent = agent
#         self.tools = {}
#         if hasattr(agent, "tools"):
#             self.tools = {
#                 "code_execution_tool": agent.tools.get("code_execution_tool"),
#                 "webpage_content_tool": agent.tools.get("webpage_content_tool"),
#             }
#         else:
#             print("Warning: Agent does not have a 'tools' attribute.")

#     async def execute(self, task, **kwargs):
#         # Check the context of the task
#         if self.is_web_interaction(task):
#             # Verificar que la herramienta esté disponible antes de llamarla
#             if not self.tools["webpage_content_tool"]:
#                 return Response(
#                     message="Error: Webpage Content Tool is not available.",
#                     break_loop=True,
#                 )
#             return await self.tools["webpage_content_tool"].execute(**kwargs)
#         elif self.is_code_execution(task):
#             # Verificar que la herramienta esté disponible antes de llamarla
#             if not self.tools["code_execution_tool"]:
#                 return Response(
#                     message="Error: Code Execution Tool is not available.",
#                     break_loop=True,
#                 )
#             return await self.tools["code_execution_tool"].execute(**kwargs)
#         else:
#             return Response(
#                 message="Error: No suitable tool found for this task.", break_loop=True
#             )

#     def is_web_interaction(self, task):
#         # Keywords that imply a web browser action
#         web_actions = ["click", "type", "search", "navigate", "scroll", "accept terms"]
#         return any(action in task.lower() for action in web_actions)

#     def is_code_execution(self, task):
#         # Keywords that imply a code execution or terminal interaction
#         code_actions = ["install", "run", "execute", "shell", "command", "terminal"]
#         return any(action in task.lower() for action in code_actions)


# class ToolRouter:
#     def __init__(self, agent):
#         self.agent = agent
#         self.tools = {}
#         if hasattr(agent, "tools"):
#             self.tools = {
#                 "code_execution_tool": agent.tools.get("code_execution_tool"),
#                 "webpage_content_tool": agent.tools.get("webpage_content_tool"),
#             }
#         else:
#             print("Warning: Agent does not have a 'tools' attribute.")

#     async def execute(self, task, **kwargs):
#         # Check the context of the task
#         if self.is_youtube_search(task):
#             # Prioritize using the webpage_content_tool for YouTube search
#             if not self.tools.get("webpage_content_tool"):
#                 return Response(
#                     message="Error: Webpage Content Tool is not available.",
#                     break_loop=True,
#                 )
#             return await self.tools["webpage_content_tool"].execute(**kwargs)
#         elif self.is_web_interaction(task):
#             # Verificar que la herramienta esté disponible antes de llamarla
#             if not self.tools.get("webpage_content_tool"):
#                 return Response(
#                     message="Error: Webpage Content Tool is not available.",
#                     break_loop=True,
#                 )
#             return await self.tools["webpage_content_tool"].execute(**kwargs)
#         elif self.is_code_execution(task):
#             # Verificar que la herramienta esté disponible antes de llamarla
#             if not self.tools.get("code_execution_tool"):
#                 return Response(
#                     message="Error: Code Execution Tool is not available.",
#                     break_loop=True,
#                 )
#             return await self.tools["code_execution_tool"].execute(**kwargs)
#         else:
#             return Response(
#                 message="Error: No suitable tool found for this task.", break_loop=True
#             )

#     def is_youtube_search(self, task):
#         # Specifically detect when the user is trying to search YouTube
#         youtube_keywords = ["search youtube", "youtube", "find on youtube"]
#         return any(keyword in task.lower() for keyword in youtube_keywords)

#     def is_web_interaction(self, task):
#         # Keywords that imply a web browser action
#         web_actions = ["click", "type", "search", "navigate", "scroll", "accept terms"]
#         return any(action in task.lower() for action in web_actions)

#     def is_code_execution(self, task):
#         # Keywords that imply a code execution or terminal interaction
#         code_actions = ["install", "run", "execute", "shell", "command", "terminal"]
#         return any(action in task.lower() for action in code_actions)









# class ToolRouter:
#     def __init__(self, agent):
#         self.agent = agent
#         self.tools = {}
#         if hasattr(agent, "tools"):
#             self.tools = {
#                 "code_execution_tool": agent.tools.get("code_execution_tool"),
#                 "webpage_content_tool": agent.tools.get("webpage_content_tool"),
#             }
#         else:
#             print("Warning: Agent does not have a 'tools' attribute.")

#     async def execute(self, task, **kwargs):
#         # Priorizar la herramienta de búsqueda web para consultas de búsqueda
#         if self.is_web_search(task):
#             if not self.tools["webpage_content_tool"]:
#                 return Response(
#                     message="Error: Webpage Content Tool is not available.",
#                     break_loop=True,
#                 )
#             return await self.tools["webpage_content_tool"].execute(**kwargs)
#         elif self.is_web_interaction(task):
#             # Si es una interacción con el navegador, usar la herramienta de contenido web
#             if not self.tools["webpage_content_tool"]:
#                 return Response(
#                     message="Error: Webpage Content Tool is not available.",
#                     break_loop=True,
#                 )
#             return await self.tools["webpage_content_tool"].execute(**kwargs)
#         elif self.is_code_execution(task):
#             # Si es una tarea de ejecución de código, usar la herramienta de ejecución de código
#             if not self.tools["code_execution_tool"]:
#                 return Response(
#                     message="Error: Code Execution Tool is not available.",
#                     break_loop=True,
#                 )
#             return await self.tools["code_execution_tool"].execute(**kwargs)
#         else:
#             return Response(
#                 message="Error: No suitable tool found for this task.", break_loop=True
#             )

#     def is_web_search(self, task):
#         # Priorizar tareas que son explícitamente de búsqueda web
#         search_actions = ["search", "find", "look for", "query", "lookup", "information on"]
#         return any(action in task.lower() for action in search_actions)

#     def is_web_interaction(self, task):
#         # Identificar si es una interacción con el navegador web
#         web_actions = ["click", "type", "navigate", "scroll", "accept terms"]
#         return any(action in task.lower() for action in web_actions)

#     def is_code_execution(self, task):
#         # Identificar si la tarea es de ejecución de código
#         code_actions = ["install", "run", "execute", "shell", "command", "terminal"]
#         return any(action in task.lower() for action in code_actions)
