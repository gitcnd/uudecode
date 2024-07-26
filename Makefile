# Define variables
MPY_CROSS = ../micropython/mpy-cross/build/mpy-cross

# Default target
all: uudecode124.mpy

# Rule to create .mpy from .py
uudecode124.mpy: uudecode.py
	$(MPY_CROSS) $< -o $@

# Clean up
clean:
	rm -f $(OUT)

# Phony targets
.PHONY: all clean

