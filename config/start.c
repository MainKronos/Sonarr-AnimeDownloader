#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <pwd.h>
#include <dirent.h>
#include <errno.h>
#include <sys/wait.h>
#include <sys/types.h>

int main(int argc, char *argv[])
{
	int status; /* Stato di uscita processo figlio */
	struct passwd* res; /* Risultato valore getpwnam */
	DIR* dir; /* Cartella */
	struct dirent* dir_inf; 

	int dbg = 0;

	char* PUID = getenv("PUID");
	if(!PUID) PUID = "1000";
	char* PGID = getenv("PGID");
	if(!PGID) PGID = "1000";
	char* USER_NAME = getenv("USER_NAME");

	if(fork()){
		wait(&status);
		if(fork()){
			wait(&status);

			res = getpwnam(USER_NAME);

			printf(
				"\n\n-------------------------------------\n"
				"GID/UID\n"
				"-------------------------------------\n"
				"User uid:\t%d\n"
				"User gid:\t%d\n"
				"-------------------------------------\n\n\n",
				res->pw_uid, res->pw_gid
			);
			if(fork()){
				wait(&status);
				if(fork()){
					wait(&status);
					if(fork()){
						wait(&status);
						if(fork()){
							wait(&status);
							if(fork()){
								wait(&status);
								if(fork()){
									wait(&status);
									if(fork()){
										wait(&status);

										chdir("/script");
										setuid(atoi(PUID));

										return system("python3 -u /script/main.py");
									} else {
										char* tmp; /* buffer */
										dir = opendir("/script/connections");
										if(!dir) exit(0);

										while(1){
											dir_inf = readdir(dir);
											if(!dir_inf) exit(0);

											if((tmp = strrchr(dir_inf->d_name, '.'))){
												if(strcmp(".sh", tmp) == 0) break;
											}
										}
										closedir(dir);

										execlp(NULL, "sed", "-i", "-e", "'s/\\r$//'", "/script/connections/*.sh", NULL);
									}
								} else execlp(NULL, "pip3", "install", "--upgrade", "--no-cache-dir", "--disable-pip-version-check", "--quiet", "animeworld", NULL);
							} else execlp(NULL, "chmod", "777", "/script", "-R", NULL);
						} else execlp(NULL, "chgrp", USER_NAME, "/script", "-R", NULL);
					} else execlp(NULL, "chown", USER_NAME, "/script", "-R", NULL);
				} else execlp(NULL, "touch", "/script/json/table.json", NULL);
			} else execlp(NULL, "touch", "/script/json/settings.json", NULL);
		} else execlp(NULL, "groupmod", "-o", "-g", PGID, USER_NAME, NULL);	
	} else execlp(NULL, "usermod", "-o", "-u", PUID, USER_NAME, NULL);

	fprintf(stderr, "ERROR %d: %s", dbg, strerror(errno));
	exit(EXIT_FAILURE);
}