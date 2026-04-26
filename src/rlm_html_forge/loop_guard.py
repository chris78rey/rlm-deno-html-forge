from __future__ import annotations
from dataclasses import dataclass, field
from time import monotonic

class LoopGuardError(RuntimeError): pass

@dataclass
class LoopGuard:
    max_depth: int
    max_calls_per_subagent: int
    max_total_calls: int
    max_money_spent: float
    max_repair_attempts: int
    max_same_error_repetitions: int
    max_seconds_per_phase: int
    input_cost_per_1m_tokens: float = 0.0
    output_cost_per_1m_tokens: float = 0.0
    total_calls: int = 0
    total_estimated_cost: float = 0.0
    phase_started_at: float = field(default_factory=monotonic)
    errors_seen: dict[str, int] = field(default_factory=dict)
    calls_by_agent: dict[str, int] = field(default_factory=dict)
    def begin_phase(self) -> None: self.phase_started_at = monotonic()
    def check_phase_timeout(self, phase_name: str) -> None:
        if monotonic() - self.phase_started_at > self.max_seconds_per_phase:
            raise LoopGuardError(f"Fase '{phase_name}' excedió {self.max_seconds_per_phase} segundos.")
    def check_depth(self, depth: int) -> None:
        if depth > self.max_depth: raise LoopGuardError(f"Profundidad RLM excedida: {depth} > {self.max_depth}")
    def register_call(self, agent_name: str, input_tokens: int = 0, output_tokens: int = 0) -> None:
        self.total_calls += 1
        self.calls_by_agent[agent_name] = self.calls_by_agent.get(agent_name, 0) + 1
        if self.total_calls > self.max_total_calls:
            raise LoopGuardError(f"Máximo total de llamadas excedido: {self.total_calls} > {self.max_total_calls}")
        if self.calls_by_agent[agent_name] > self.max_calls_per_subagent:
            raise LoopGuardError(f"Máximo de llamadas para {agent_name} excedido")
        self.total_estimated_cost += ((input_tokens/1_000_000)*self.input_cost_per_1m_tokens + (output_tokens/1_000_000)*self.output_cost_per_1m_tokens)
        if self.total_estimated_cost > self.max_money_spent:
            raise LoopGuardError(f"Presupuesto excedido: {self.total_estimated_cost:.6f} > {self.max_money_spent:.6f}")
    def register_error(self, error_message: str) -> None:
        key = error_message.strip()[:300]
        self.errors_seen[key] = self.errors_seen.get(key, 0) + 1
        if self.errors_seen[key] > self.max_same_error_repetitions:
            raise LoopGuardError(f"Error repetido demasiadas veces: {key}")
    def check_repair_attempt(self, attempt: int) -> None:
        if attempt > self.max_repair_attempts:
            raise LoopGuardError(f"Máximo de intentos de reparación excedido: {attempt} > {self.max_repair_attempts}")
