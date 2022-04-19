#ifndef _PLUG_SETUP_H_INCLUDE_
#define _PLUG_SETUP_H_INCLUDE_

int mqtt_setup();
int network_setup();
char* get_mqttDataTopicStr();
char* get_mqttCtrlTopicStr();

#endif
