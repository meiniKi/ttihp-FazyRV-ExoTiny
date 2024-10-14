# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0
# Modifications © 2024 Meinhard Kissich

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Event, ClockCycles, RisingEdge, FallingEdge, Timer

finish_or_fatal_event = Event()

@cocotb.test()
async def test(dut):
  dut._log.info("Start")
  
  ## Our example module doesn't use clock and reset, but we show how to use them here anyway.
  clock = Clock(dut.clk, 10, units="us")
  cocotb.start_soon(clock.start())

  ## Reset
  dut._log.info("Reset")
  dut.rst_n.value = 0
  await ClockCycles(dut.clk, 20)
  await Timer(1, units="us")
  dut.rst_n.value = 1

  await ClockCycles(dut.clk, 20)
  assert dut.test_done.value.binstr != "x"

  await RisingEdge(dut.test_done)
  await FallingEdge(dut.clk)
  assert dut.test_pass.value == 1