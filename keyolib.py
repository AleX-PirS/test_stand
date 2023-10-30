import keyoscacquire as koa

scope = koa.Oscilloscope(address="TCPIP::10.3.69.148::INSTR", timeout=30000)

time, y, chennels = scope.get_trace(channels=[1])

print(time, y, chennels)