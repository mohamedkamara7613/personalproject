# Compiler and Flags
CC = gcc
CFLAGS = -Wall -Wextra -g -Iinclude -Iinclude/algo -Iinclude/elec

# Directories
SRC_DIR = src
SRC_ALGO = src/algo
SRC_ELEC = src/elec
BIN_DIR = bin
DOC_DIR = doc
TEST_DIR = tests

# Source Files
SRCS_ALGO = $(wildcard $(SRC_ALGO)/*.c)
SRCS_ELEC = $(wildcard $(SRC_ELEC)/*.c)

MAINS = $(SRC_ALGO)/path_optim.c $(SRC_ALGO)/simulator.c $(SRC_DIR)/test_communication.c

# We generate .o files NEXT to the .c files
OBJS_ALGO = $(filter-out $(SRC_ALGO)/path_optim.o $(SRC_ALGO)/simulator.o $(SRC_ALGO)/test_%.o, $(SRCS_ALGO:.c=.o))
OBJS_ELEC = $(SRCS_ELEC:.c=.o)

# Test Sources
TEST_SRCS = $(wildcard $(SRC_ALGO)/test_*.c)
TEST_BINS = $(patsubst $(SRC_ALGO)/%.c, $(TEST_DIR)/%, $(TEST_SRCS))

# Targets
TARGET_OPTIM = $(BIN_DIR)/path_optim
TARGET_MAIN_ELEC = $(BIN_DIR)/main_elec

# Default Target (All)
all: create_dirs prg tests doc

# Prg: Compile main programs
prg: $(TARGET_OPTIM) $(TARGET_MAIN_ELEC)

# Tests: Compile all tests found in tests/
tests: $(TEST_BINS)

# Doc: Generate documentation
doc:
	@if command -v doxygen > /dev/null; then \
		doxygen Doxyfile; \
	else \
		echo "Doxygen not found. Skipping documentation generation."; \
	fi

# Linking Main Programs
$(TARGET_OPTIM): $(SRC_ALGO)/path_optim.o $(OBJS_ALGO) | create_dirs
	$(CC) $(CFLAGS) -o $@ $^

$(BIN_DIR)/main_elec: $(SRC_ELEC)/main_elec.o $(OBJS_ELEC) | create_dirs
	$(CC) $(CFLAGS) -o $@ $^ -lwiringPi -lwiringPiDev -lm

# Linking Tests
$(TEST_DIR)/test_%: $(SRC_ALGO)/test_%.c $(OBJS_ALGO) | create_dirs
	$(CC) $(CFLAGS) -o $@ $< $(OBJS_ALGO) -lcunit

# Compile Source Files
# %.o depends on %.c
$(SRC_ALGO)/%.o: $(SRC_ALGO)/%.c
	$(CC) $(CFLAGS) -c $< -o $@

$(SRC_ELEC)/%.o: $(SRC_ELEC)/%.c
	$(CC) $(CFLAGS) -c $< -o $@

$(SRC_DIR)/%.o: $(SRC_DIR)/%.c
	$(CC) $(CFLAGS) -c $< -o $@

$(TEST_DIR)/%.o: $(TEST_DIR)/%.c
	$(CC) $(CFLAGS) -c $< -o $@

# Create Directories
create_dirs:
	@mkdir -p $(BIN_DIR) $(DOC_DIR) $(TEST_DIR)

# Clean
clean:
	rm -f $(SRC_ALGO)/*.o $(SRC_ELEC)/*.o $(SRC_DIR)/*.o $(TEST_DIR)/*.o
	rm -rf $(BIN_DIR) $(DOC_DIR)/html $(DOC_DIR)/latex
# Phony Targets
.PHONY: all prg tests doc clean create_dirs
