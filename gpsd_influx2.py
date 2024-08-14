#!/usr/bin/python3
from gps import *
from time import *
import getopt
import os
import socket
import sys
import threading
import time

from pprint import pprint

# Your InfluxDB Settings
from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

bucket = "gpsd"

# Number of seconds between updates
update_interval = 10

# --------------------------------------------------------------------------------
# Do not change anything below this line
hostname = socket.gethostname()

# --------------------------------------------------------------------------------
# Command Line Options

debug = None
detailed_sats = None
output = True

if "-d" in sys.argv:
    debug = True
if "-s" in sys.argv:
    detailed_sats = True
if "-o" in sys.argv:
    output = None

# --------------------------------------------------------------------------------
# GPS Thread
class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd
    gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)
    self.current_value = None
    self.running = True

  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next()

# --------------------------------------------------------------------------------
# GPS Loop
if __name__ == '__main__':
    with InfluxDBClient.from_config_file("config.ini") as client:
        # Create the thread
        gpsp = GpsPoller()
        try:
            # Start up the thread
            gpsp.start()

            # Sleep for 5 seconds to allow the gps to pick up the position
            time.sleep(5)

            # Start the loop
            while True:
                gpsd_alt   = float(gpsd.fix.altitude)
                gpsd_climb = float(gpsd.fix.climb)
                gpsd_epc   = float(gpsd.fix.epc)
                gpsd_eps   = float(gpsd.fix.eps)
                gpsd_ept   = float(gpsd.fix.ept)
                gpsd_epv   = float(gpsd.fix.epv)
                gpsd_epx   = float(gpsd.fix.epx)
                gpsd_epy   = float(gpsd.fix.epy)
                gpsd_lat   = float(gpsd.fix.latitude)
                gpsd_lon   = float(gpsd.fix.longitude)
                gpsd_mode  = float(gpsd.fix.mode)
                gpsd_status  = int(gpsd.fix.status)
                gpsd_speed = float(gpsd.fix.speed)
                gpsd_track = float(gpsd.fix.track)
                gpsd_sats_vis = int(len(gpsd.satellites))
                gpsd_sats_used = int(gpsd.satellites_used)

                # combined status field, 0-4 = ZERO, NO_FIX, 2D, 3D, DGPS
                gpsd_status_combined = gpsd_mode
                if gpsd_status == 2 and gpsd_mode == 3:
                    gpsd_status_combined = 4.0

                # Make sure we have a lat, lon and alt
                if debug == True:
                    print("gpsd-python,host=",hostname,",tpv=alt value=",gpsd_alt)
                    print("gpsd-python,host=",hostname,",tpv=climb value=",gpsd_climb)
                    print("gpsd-python,host=",hostname,",tpv=epc value=",gpsd_epc)
                    print("gpsd-python,host=",hostname,",tpv=eps value=",gpsd_eps)
                    print("gpsd-python,host=",hostname,",tpv=ept value=",gpsd_ept)
                    print("gpsd-python,host=",hostname,",tpv=epv value=",gpsd_epv)
                    print("gpsd-python,host=",hostname,",tpv=epx value=",gpsd_epx)
                    print("gpsd-python,host=",hostname,",tpv=epy value=",gpsd_epy)
                    print("gpsd-python,host=",hostname,",tpv=lat value=",gpsd_lat)
                    print("gpsd-python,host=",hostname,",tpv=lon value=",gpsd_lon)
                    print("gpsd-python,host=",hostname,",tpv=mode value=",gpsd_mode)
                    print("gpsd-python,host=",hostname,",tpv=speed value=",gpsd_speed)
                    print("gpsd-python,host=",hostname,",tpv=track value=",gpsd_track)
                    print("gpsd-python,host=",hostname,",sats_vis value=",gpsd_sats_vis)
                    print("gpsd-python,host=",hostname,",sats_used value=",gpsd_sats_used)
                    print("gpsd-python,host=",hostname,",status value=",gpsd_status)
                    print("gpsd-python,host=",hostname,",status_combined value=",gpsd_status_combined)
                    pprint(gpsd)
                    if detailed_sats == True:
                        pprint(gpsd.satellites)

                write_api = client.write_api(write_options=SYNCHRONOUS)
                points = []
                if not math.isnan(gpsd_alt):
                    p = Point("gpsd").tag("host", hostname).field("alt", gpsd_alt)
                    points.append(p)
                if not math.isnan(gpsd_climb):
                    p = Point("gpsd").tag("host", hostname).field("climb", gpsd_climb)
                    points.append(p)
                if not math.isnan(gpsd_epc):
                    p = Point("gpsd").tag("host", hostname).field("epc", gpsd_epc)
                    points.append(p)
                if not math.isnan(gpsd_eps):
                    p = Point("gpsd").tag("host", hostname).field("eps", gpsd_eps)
                    points.append(p)
                if not math.isnan(gpsd_ept):
                    p = Point("gpsd").tag("host", hostname).field("ept", gpsd_ept)
                    points.append(p)
                if not math.isnan(gpsd_epv):
                    p = Point("gpsd").tag("host", hostname).field("epv", gpsd_epv)
                    points.append(p)
                if not math.isnan(gpsd_epx):
                    p = Point("gpsd").tag("host", hostname).field("epx", gpsd_epx)
                    points.append(p)
                if not math.isnan(gpsd_epy):
                    p = Point("gpsd").tag("host", hostname).field("epy", gpsd_epy)
                    points.append(p)
                if not math.isnan(gpsd_lat):
                    p = Point("gpsd").tag("host", hostname).field("lat", gpsd_lat)
                    points.append(p)
                if not math.isnan(gpsd_lon):
                    p = Point("gpsd").tag("host", hostname).field("lon", gpsd_lon)
                    points.append(p)
                if not math.isnan(gpsd_mode):
                    p = Point("gpsd").tag("host", hostname).field("mode", gpsd_mode)
                    points.append(p)
                if not math.isnan(gpsd_speed):
                    p = Point("gpsd").tag("host", hostname).field("speed", gpsd_speed)
                    points.append(p)
                if not math.isnan(gpsd_track):
                    p = Point("gpsd").tag("host", hostname).field("track", gpsd_track)
                    points.append(p)
                if not math.isnan(gpsd_status):
                    p = Point("gpsd").tag("host", hostname).field("status", gpsd_status)
                    points.append(p)
                if not math.isnan(gpsd_status_combined):
                    p = Point("gpsd").tag("host", hostname).field("status_combined", gpsd_status_combined)
                    points.append(p)
                if not math.isnan(gpsd_sats_vis):
                    p = Point("gpsd").tag("host", hostname).tag("gnss_system", "all").field("sats_vis", gpsd_sats_vis)
                    points.append(p)
                if not math.isnan(gpsd_sats_used):
                    p = Point("gpsd").tag("host", hostname).tag("gnss_system", "all").field("sats_used", gpsd_sats_used)
                    points.append(p)
                if detailed_sats == True:
                    gps_count = 0
                    sbas_count = 0
                    glonass_count = 0
                    qszz_count = 0
                    galileo_count = 0
                    beidou_count = 0
                    tracked_gps_count = 0
                    tracked_sbas_count = 0
                    tracked_glonass_count = 0
                    tracked_qszz_count = 0
                    tracked_galileo_count = 0
                    tracked_beidou_count = 0
                    for sat in gpsd.satellites:
                        # probably not the optimal way to do it, but gpsd isn't super well documented and I'm not good at python
                        # "PRN:   2  E:  19  Az: 244  Ss:  24  Used: y"
                        # ideally we should also split off by system, and by SBAS or not?
                        satparms = str(sat).split()
                        prn = int(satparms[1])
                        prn_str = ""
                        # https://gpsd.gitlab.io/gpsd/gpsd_json.html gives a bit of a clue here?
                        # PRN ID of the satellite. 1-63 are GNSS satellites, 64-96 are GLONASS satellites, 100-164 are SBAS satellites
                        # however, it does not specify what happens with Galileo or Beidou?
                        # and then we finally find in driver_nmea0183.c
                        #     *   1..32:  GPS
                        #     *   33..64: Various SBAS systems (EGNOS, WAAS, SDCM, GAGAN, MSAS)
                        #     *   65..96: GLONASS
                        #     *   101..136: Quectel Querk, (not NMEA), seems to be Galileo
                        #     *   152..158: Various SBAS systems (EGNOS, WAAS, SDCM, GAGAN, MSAS)
                        #     *   173..182: IMES
                        #     *   193..202: QZSS   (u-blox extended 4.10)
                        #     *   201..264: BeiDou (not NMEA, not u-blox?) Quectel Querk.
                        #     *   301..336: Galileo
                        #     *   401..437: BeiDou
                        #     *   null: GLONASS unused
                        #     *   500-509: NavIC (IRNSS)  NOT STANDARD!
                        # at the risk of pissing someone off, it's funny how ESR wrote a big rant about lacking documentation from GPS vendors
                        # given how I keep having to dig around in the source code of gpsd

                        satused = 0;
                        if "y" in satparms[9]:
                            satused = 1

                        gnss_system = ""

                        if prn <= 32:
                            prn_str = "GP"+str(prn)
                            gps_count += 1
                            if satused == 1:
                                tracked_gps_count += 1
                            gnss_system = "NavStar"
                        elif prn >= 33 and prn <= 64:
                            # SBAS stuff is offset -87 for some reason
                            prn_str = "S"+str(prn+87)
                            sbas_count += 1
                            if satused == 1:
                                tracked_sbas_count += 1
                            gnss_system = "SBAS"
                        elif prn >= 65 and prn <= 96:
                            # GLONASS is offset +64
                            prn_str = "GL"+str(prn-64)
                            glonass_count += 1
                            if satused == 1:
                                tracked_glonass_count += 1
                            gnss_system = "GLONASS"
                        elif prn >= 152 and prn <= 158:
                            prn_str = "S"+str(prn)
                            sbas_count += 1
                            if satused == 1:
                                tracked_sbas_count += 1
                            gnss_system = "SBAS"
                        elif prn >= 193 and prn <= 202:
                            # QSZZ is offset +64
                            prn_str = "QS"+str(prn-192)
                            qszz_count += 1
                            if satused == 1:
                                tracked_qszz_count += 1
                            gnss_system = "QSZZ"
                        elif prn >= 201 and prn <= 264:
                            # BeiDou is offset +200
                            prn_str = "B"+str(prn-200)
                            beidou_count += 1
                            if satused == 1:
                                tracked_beidou_count += 1
                            gnss_system = "BeiDou"
                        elif prn >= 301 and prn <= 336:
                            # Galileo is offset +300
                            prn_str = "GA"+str(prn-300)
                            galileo_count += 1
                            if satused == 1:
                                tracked_galileo_count += 1
                            gnss_system = "Galileo"
                        elif prn >= 401 and prn <= 437:
                            # More BeiDou offset +400
                            prn_str = "B"+str(prn-400)
                            beidou_count += 1
                            if satused == 1:
                                tracked_beidou_count += 1
                            gnss_system = "BeiDou"

                        p = Point("gpsd_sat_details").tag("host", hostname).tag("prn", prn_str).tag("gnss_system", gnss_system).field("ele", int(satparms[3]))
                        points.append(p)
                        p = Point("gpsd_sat_details").tag("host", hostname).tag("prn", prn_str).tag("gnss_system", gnss_system).field("azi", int(satparms[5]))
                        points.append(p)
                        p = Point("gpsd_sat_details").tag("host", hostname).tag("prn", prn_str).tag("gnss_system", gnss_system).field("snr", int(satparms[7]))
                        points.append(p)
                        p = Point("gpsd_sat_details").tag("host", hostname).tag("prn", prn_str).tag("gnss_system", gnss_system).field("used", int(satused))
                        points.append(p)
                        if debug == True:
                            print(prn_str + " " + gnss_system)
                    
                    p = Point("gpsd").tag("host", hostname).tag("gnss_system", "NavStar").field("sats_used", tracked_gps_count)
                    points.append(p)
                    p = Point("gpsd").tag("host", hostname).tag("gnss_system", "NavStar").field("sats_vis", gps_count)
                    points.append(p)

                    p = Point("gpsd").tag("host", hostname).tag("gnss_system", "SBAS").field("sats_used", tracked_sbas_count)
                    points.append(p)
                    p = Point("gpsd").tag("host", hostname).tag("gnss_system", "SBAS").field("sats_vis", sbas_count)
                    points.append(p)

                    p = Point("gpsd").tag("host", hostname).tag("gnss_system", "GLONASS").field("sats_used", tracked_glonass_count)
                    points.append(p)
                    p = Point("gpsd").tag("host", hostname).tag("gnss_system", "GLONASS").field("sats_vis", glonass_count)
                    points.append(p)

                    p = Point("gpsd").tag("host", hostname).tag("gnss_system", "QSZZ").field("sats_used", tracked_qszz_count)
                    points.append(p)
                    p = Point("gpsd").tag("host", hostname).tag("gnss_system", "QSZZ").field("sats_vis", qszz_count)
                    points.append(p)

                    p = Point("gpsd").tag("host", hostname).tag("gnss_system", "BeiDou").field("sats_used", tracked_beidou_count)
                    points.append(p)
                    p = Point("gpsd").tag("host", hostname).tag("gnss_system", "BeiDou").field("sats_vis", beidou_count)
                    points.append(p)

                    p = Point("gpsd").tag("host", hostname).tag("gnss_system", "Galileo").field("sats_used", tracked_galileo_count)
                    points.append(p)
                    p = Point("gpsd").tag("host", hostname).tag("gnss_system", "Galileo").field("sats_vis", galileo_count)
                    points.append(p)

                    # assume that if we have SBAS and a 3D fix, then we're DGPS fixed
                    if tracked_sbas_count > 0 or tracked_qszz_count > 0 and gpsd_mode == 3:
                        p = Point("gpsd").tag("host", hostname).field("fixstatus_modified", 4)
                        points.append(p)
                    else:
                        p = Point("gpsd").tag("host", hostname).field("fixstatus_modified", int(gpsd_mode))
                        points.append(p)

                if output == True:
                    write_api.write(bucket=bucket, record=points)

                
                time.sleep(update_interval)
        except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
            print ("\nKilling Thread...")
            gpsp.running = False
            gpsp.join() # wait for the thread to finish what it's doing
            print ("Done.\nExiting.")
        except:
            print ("Something went wrong, probably gpsd or influx died. Terminating.")
            gpsp.running = False
            gpsp.join() # wait for the thread to finish what it's doing
            sys.exit(1) # exit with error code
