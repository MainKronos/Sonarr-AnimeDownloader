#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <pwd.h>
#include <dirent.h>
#include <errno.h>
#include <sys/wait.h>
#include <sys/types.h>

int start(){
	char command[500]; /* Buffer per i comandi system */
	struct passwd* pwn; /* Risultato valore getpwnam */
	int res; /* Risposta System */

	char* PUID = getenv("PUID");
	if(!PUID) PUID = "1000";
	char* PGID = getenv("PGID");
	if(!PGID) PGID = "1000";
	char* USER_NAME = getenv("USER_NAME");

	sprintf(command, "usermod -o -u %s %s", PUID, USER_NAME);
	res = system(command);
	if(res) return res;

	sprintf(command, "groupmod -o -g %s %s", PGID, USER_NAME);
	res = system(command);
	if(res) return res;

	pwn = getpwnam(USER_NAME);
	printf(
		"\n\n-------------------------------------\n"
		"GID/UID\n"
		"-------------------------------------\n"
		"User uid:\t%d\n"
		"User gid:\t%d\n"
		"-------------------------------------\n\n\n",
		pwn->pw_uid, pwn->pw_gid
	);

	strcpy(command, "touch /script/json/settings.json");
	res = system(command);
	if(res) return res;

	strcpy(command, "touch /script/json/table.json");
	res = system(command);
	if(res) return res;

	sprintf(command, "chown %s:%s /script -R", USER_NAME, USER_NAME);
	res = system(command);
	if(res) return res;

	strcpy(command, "chmod 777 /script -R");
	res = system(command);
	if(res) return res;

	strcpy(command, "pip3 install --upgrade --no-cache-dir --disable-pip-version-check --quiet animeworld");
	res = system(command);
	if(res) return res;

	char* tmp; /* buffer */
	DIR* dir = opendir("/script/connections");
	if(dir){
		struct dirent* dir_inf; 

		while(1){
			dir_inf = readdir(dir);
			if(!dir_inf) break;

			if((tmp = strrchr(dir_inf->d_name, '.'))){
				if(strcmp(".sh", tmp) == 0){
					system("sed -i -e 's/\\r$//' /script/connections/*.sh");
					break;
				}
			}
		}
		closedir(dir);
	}

	chdir("/script");
	setuid(atoi(PUID));
	
	return system("python3 -u /script/main.py");
}

int main(int argc, char *argv[])
{
	int res = start();
	if(res){
		fprintf(stderr, "ERROR: %s", strerror(errno));
		exit(EXIT_FAILURE);
	}
	return 0;
}