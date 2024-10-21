from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import asyncio

class BaseAgent(Agent):
    class InformBehav(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                print(f"Agent {self.agent.name} received: {msg.body}")
            else:
                print(f"Agent {self.agent.name} didn't receive any message after 10 seconds")

    async def setup(self):
        print(f"Agent {self.name} starting...")
        b = self.InformBehav()
        self.add_behaviour(b)

class TaskAgent(BaseAgent):
    async def setup(self):
        await super().setup()
        self.add_behaviour(self.TaskBehaviour())

    class TaskBehaviour(CyclicBehaviour):
        async def run(self):
            print(f"Agent {self.agent.name} is performing a task")
            await asyncio.sleep(5)

def create_agent(name, password, agent_class=BaseAgent):
    agent = agent_class(f"{name}@localhost", password)
    future = agent.start()
    future.result()
    return agent
