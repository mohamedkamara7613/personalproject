JAVAC = javac
JAVA = java
SRC_DIR = src
TEST_DIR = srctest
BIN_DIR = classes
TEST_BIN_DIR = classestest
LIB_DIR = lib

CP_SEP = :
JUNIT_JAR = $(LIB_DIR)/junit4.jar
HAMCREST_JAR = $(LIB_DIR)/hamcrest-all.jar

# les classpaths
COMPILE_CP = $(SRC_DIR)
TEST_COMPILE_CP = $(BIN_DIR)$(CP_SEP)$(JUNIT_JAR)$(CP_SEP)$(HAMCREST_JAR)
TEST_RUN_CP = $(TEST_BIN_DIR)$(CP_SEP)$(BIN_DIR)$(CP_SEP)$(JUNIT_JAR)$(CP_SEP)$(HAMCREST_JAR)

# Nouveaux variables pour les tests du professeur
TEST_PROF_DIR = classestest_prof
TEST_PROF_CP = $(TEST_PROF_DIR)$(CP_SEP)$(BIN_DIR)$(CP_SEP)$(JUNIT_JAR)$(CP_SEP)$(HAMCREST_JAR)

# recup des fichiers sources
SOURCES = $(shell find $(SRC_DIR) -name "*.java")
TEST_SOURCES = $(shell find $(TEST_DIR) -name "*.java")

# la lise des classes qu'on est censé avoir
CLASSES = $(SOURCES:$(SRC_DIR)/%.java=$(BIN_DIR)/%.class)
TEST_CLASSES = $(TEST_SOURCES:$(TEST_DIR)/%.java=$(TEST_BIN_DIR)/%.class)

.PHONY: all clean run-tests build build-tests run-tests-prof test-prof-serrure test-prof-porte-serrure test-prof-monstre test-prof-piece test-prof-vivant run-main

all: build build-tests

# Compilation des sources sans les tests
build: $(CLASSES)

# -Xlint:unchecked
$(BIN_DIR)/%.class: $(SRC_DIR)/%.java
	@mkdir -p $(BIN_DIR)
	$(JAVAC) -d $(BIN_DIR) -sourcepath $(SRC_DIR)  $<

# Compilation de l'ensemble (optimisé avec un fichier texte des sources)
compile-all:
	@mkdir -p $(BIN_DIR)
	find $(SRC_DIR) -name "*.java" > sources_list.txt
	$(JAVAC) -d $(BIN_DIR) @sources_list.txt
	@rm -f sources_list.txt

# Compilation des tests
build-tests: compile-all $(TEST_CLASSES)

$(TEST_BIN_DIR)/%.class: $(TEST_DIR)/%.java
	@mkdir -p $(TEST_BIN_DIR)
	$(JAVAC) -cp "$(TEST_COMPILE_CP)" -d $(TEST_BIN_DIR) -sourcepath $(TEST_DIR) $<

compile-tests-all: compile-all
	@mkdir -p $(TEST_BIN_DIR)
	find $(TEST_DIR) -name "*.java" > test_sources_list.txt
	$(JAVAC) -cp "$(TEST_COMPILE_CP)" -d $(TEST_BIN_DIR) @test_sources_list.txt
	@rm -f test_sources_list.txt

# Exécution complète de tous les tests (locaux)
run-tests: compile-tests-all
	$(JAVA) -cp "$(TEST_RUN_CP)" org.junit.runner.JUnitCore fr.insarouen.iti.prog.aventure.AllTests

# --- Cibles pour les tests du professeur ---

# Lancer TOUS les tests du prof
run-tests-prof: build 
	$(JAVA) -cp "$(TEST_PROF_CP)" org.junit.runner.JUnitCore fr.insarouen.iti.prog.aventure.AllTests

# Lancer uniquement TestSerrure
test-prof-serrure: build
	$(JAVA) -cp "$(TEST_PROF_CP)" org.junit.runner.JUnitCore fr.insarouen.iti.prog.aventure.elements.objets.serrurerie.TestSerrure

# Lancer uniquement TestPorteAvecSerrure
test-prof-porte-serrure: build
	$(JAVA) -cp "$(TEST_PROF_CP)" org.junit.runner.JUnitCore fr.insarouen.iti.prog.aventure.elements.structure.TestPorteAvecSerrure

# Lancer uniquement TestMonstre
test-prof-monstre: build
	$(JAVA) -cp "$(TEST_PROF_CP)" org.junit.runner.JUnitCore fr.insarouen.iti.prog.aventure.elements.vivants.TestMonstre

# Lancer uniquement TestPiece
test-prof-piece: build
	$(JAVA) -cp "$(TEST_PROF_CP)" org.junit.runner.JUnitCore fr.insarouen.iti.prog.aventure.elements.structure.TestPiece

# Lancer uniquement TestVivant
test-prof-vivant: build
	$(JAVA) -cp "$(TEST_PROF_CP)" org.junit.runner.JUnitCore fr.insarouen.iti.prog.aventure.elements.vivants.TestVivant

# Lancer le jeu principal
run-main: build
	$(JAVA) -cp "$(BIN_DIR)" fr.insarouen.iti.prog.aventure.Main

# Nettoyage des dossiers générés localement (ne supprime PAS classestest_prof)
clean:
	rm -rf $(BIN_DIR)/*
	rm -rf $(TEST_BIN_DIR)/*

