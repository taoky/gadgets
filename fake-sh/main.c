/***************************************************************************/ /**

  @file         main.c

  @author       Stephen Brennan

  @date         Thursday,  8 January 2015

  @brief        LSH (Libstephen SHell)

*******************************************************************************/

// fake `sh` modified by taoky

#include <sys/wait.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

/*
  Function Declarations for builtin shell commands:
 */
int lsh_ls(char **args);
int lsh_cat(char **args);
int lsh_sh(char **args);
int lsh_help(char **args);
int lsh_exit(char **args);

/*
  List of builtin commands, followed by their corresponding functions.
 */
char *builtin_str[] = {
    "ls",
    "cat",
    "sh",
    "/bin/ls",
    "/bin/cat",
    "/bin/sh",
    "exit"};

int (*builtin_func[])(char **) = {
    &lsh_ls,
    &lsh_cat,
    &lsh_sh,
    &lsh_ls,
    &lsh_cat,
    &lsh_sh,
    &lsh_exit};

int lsh_num_builtins()
{
  return sizeof(builtin_str) / sizeof(char *);
}

int lsh_real_launch(char **args)
{
  pid_t pid;
  int status;

  pid = fork();
  if (pid == 0)
  {
    // Child process
    if (execvp(args[0], args) == -1)
    {
      perror("sh");
    }
    exit(EXIT_FAILURE);
  }
  else if (pid < 0)
  {
    // Error forking
    perror("sh");
  }
  else
  {
    // Parent process
    do
    {
      waitpid(pid, &status, WUNTRACED);
    } while (!WIFEXITED(status) && !WIFSIGNALED(status));
  }

  return 1;
}

/*
  Builtin function implementations.
*/

int lsh_ls(char **args)
{
  lsh_real_launch(args);
  return 1;
}

int lsh_cat(char **args)
{
  if (args[1] == NULL || strcmp(args[1], "flag") != 0 || args[2] != NULL)
  {
    fprintf(stderr, "cat: supports `cat flag` only.\n");
    return 1;
  }
  lsh_real_launch(args);
  return 1;
}

int lsh_sh(char **args)
{
  fprintf(stderr, "sh: restricted\n");
  return 1;
}

/**
   @brief Builtin command: exit.
   @param args List of args.  Not examined.
   @return Always returns 0, to terminate execution.
 */
int lsh_exit(char **args)
{
  return 0;
}

/**
  @brief Launch a program and wait for it to terminate.
  @param args Null terminated list of arguments (including program).
  @return Always returns 1, to continue execution.
 */
int lsh_launch(char **args)
{
  fprintf(stderr, "sh: %s: restricted\n", args[0]);

  return 1;
}

/**
   @brief Execute shell built-in or launch program.
   @param args Null terminated list of arguments.
   @return 1 if the shell should continue running, 0 if it should terminate
 */
int lsh_execute(char **args)
{
  int i;

  if (args[0] == NULL)
  {
    // An empty command was entered.
    return 1;
  }

  for (i = 0; i < lsh_num_builtins(); i++)
  {
    if (strcmp(args[0], builtin_str[i]) == 0)
    {
      return (*builtin_func[i])(args);
    }
  }

  return lsh_launch(args);
}

#define LSH_RL_BUFSIZE 1024
/**
   @brief Read a line of input from stdin.
   @return The line from stdin.
 */
char *lsh_read_line(void)
{
  int bufsize = LSH_RL_BUFSIZE;
  int position = 0;
  char *buffer = malloc(sizeof(char) * bufsize);
  int c;

  if (!buffer)
  {
    fprintf(stderr, "sh: allocation error\n");
    exit(EXIT_FAILURE);
  }

  while (1)
  {
    // Read a character
    c = getchar();

    if (c == EOF)
    {
      puts("");
      exit(0);
    }

    // If we hit EOF, just exit.
    // if (c == EOF || c == '\n') {
    if (c == '\n')
    {
      buffer[position] = '\0';
      return buffer;
    }
    else
    {
      buffer[position] = c;
    }
    position++;

    // If we have exceeded the buffer, reallocate.
    if (position >= bufsize)
    {
      bufsize += LSH_RL_BUFSIZE;
      buffer = realloc(buffer, bufsize);
      if (!buffer)
      {
        fprintf(stderr, "sh: allocation error\n");
        exit(EXIT_FAILURE);
      }
    }
  }
}

#define LSH_TOK_BUFSIZE 64
#define LSH_TOK_DELIM " \t\r\n\a"
/**
   @brief Split a line into tokens (very naively).
   @param line The line.
   @return Null-terminated array of tokens.
 */
char **lsh_split_line(char *line)
{
  int bufsize = LSH_TOK_BUFSIZE, position = 0;
  char **tokens = malloc(bufsize * sizeof(char *));
  char *token;

  if (!tokens)
  {
    fprintf(stderr, "sh: allocation error\n");
    exit(EXIT_FAILURE);
  }

  token = strtok(line, LSH_TOK_DELIM);
  while (token != NULL)
  {
    tokens[position] = token;
    position++;

    if (position >= bufsize)
    {
      bufsize += LSH_TOK_BUFSIZE;
      tokens = realloc(tokens, bufsize * sizeof(char *));
      if (!tokens)
      {
        fprintf(stderr, "sh: allocation error\n");
        exit(EXIT_FAILURE);
      }
    }

    token = strtok(NULL, LSH_TOK_DELIM);
  }
  tokens[position] = NULL;
  return tokens;
}

/**
   @brief Loop getting input and executing it.
 */
void lsh_loop(void)
{
  char *line;
  char **args;
  int status;

  do
  {
    // printf("$ ");
    line = lsh_read_line();
    args = lsh_split_line(line);
    status = lsh_execute(args);

    free(line);
    free(args);
  } while (status);
}

/**
   @brief Main entry point.
   @param argc Argument count.
   @param argv Argument vector.
   @return status code
 */
int main(int argc, char **argv)
{
  if (argc > 1)
  {
    if (argc >= 3 && strcmp(argv[1], "-c") == 0)
    {
      /* now supports:
         system("sh"); system("/bin/sh");
         system("cat flag"); system("/bin/cat flag");
         system("ls [OPTION]... [FILE]...")
         in chrooted environment.
      */
      if (strcmp(argv[2], "sh") == 0 || strcmp(argv[2], "/bin/sh") == 0)
      {
        /* `sh -c /bin/sh` or `sh -c sh` */
        /* arguments after sh are ignored */
        goto exec;
      }
      else if (strcmp(argv[2], "cat") == 0 || strcmp(argv[2], "/bin/cat") == 0)
      {
        /* `sh -c /bin/cat xxx` or `sh -c cat xxx` */
        lsh_cat(argv + 2);
      }
      else if (strcmp(argv[2], "ls") == 0 || strcmp(argv[2], "/bin/ls") == 0)
      {
        /* `sh -c /bin/ls xxx` or `sh -c ls xxx` */
        lsh_ls(argv + 2);
      }
      else
      {
        lsh_launch(argv + 2); // jmp to fake launch function
      }
    }
    else
    {
      fprintf(stderr, "sh: illegal option\n");
    }
    exit(0);
  }
exec:
  lsh_loop();

  return EXIT_SUCCESS;
}
