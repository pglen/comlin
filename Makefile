#
# Make a Community Linux jump drive
# Distributed under Community Linux Public License Version 1.0
#
# Notes:
#
#  This project assumes CentOS 6.3 file layout. It is a common 
#  system layout (Fedora, RedHat and derivates), but in some cases
#  the paths may need be adjusted.
# 
#  Dangerous scripts. Make sure you are not partitionaing drives that 
#  are in use, or drives that contain valuable data. Some rudimantary
#  checks are implemented, like refusing to partition a device
#  that is mounted on a system mount point. (/ /mnt /boot /home etc ...)
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
#  FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER 
#  IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION 
#  WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

all: 
	@echo "Type 'make help' for a list of targets"
	
help:
	@echo 
	@echo "Making a bootable jump drive. **(see Warning)"
	@echo 
	@echo "	 	make detect     -- Configure which drive is your jump drive"
	@echo "	 	make new        -- & Fdisk / Format new usb"
	@echo "	 	make copyusb    -- & @ Copy LINUX files to USB drive "
	@echo "	 	make putkern    -- & @ * Copy kernel from build dir to USB"
	@echo "	 	make syslin     -- & @ * Install syslinux to USB"
	@echo "	 	make umount     -- & @ * Unmount USB drives"
	@echo "	 	make cycle      --  Do all denoted by '*'"
	@echo "	 	make bigcycle   --  Do all denoted by '@'"
	@echo "	 	make doall      --  Do all denoted by '&'"
	@echo 
	@echo "   For more information type 'make help2'"
	@echo   
	@echo " **Warning! Make sure config_build:RDDEV points to a jump drive!" 
	@echo "      !!!! Specifying the wrong drive will destroy data !!!! " 
	@echo 

help2:
	@echo 
	@echo "Making a bootable jump drive. *(see Warning! at end)"
	@echo 
	@echo "Development / sys:"
	@echo 
	@echo "	 	make cycle       -- run putkern->syslinux->unmount"
	@echo "	 	make getusb      -- get USB content back to project"
	@echo "	 	make getusblite  -- get USB lite content back to project"
	@echo "	 	make getusb2     -- update from USB content back to project"
	@echo "	 	make copy        -- to mirror current system to USB (advanced)"
	@echo "	 	make initrd      -- to make a new initrd (obsolete)"
	@echo "	 	make initfs      -- to make a new initramfs"
	@echo "	 	make putmods     -- Copy modules from build dir to USB"
	@echo "	 	make refresh     -- Refresh kernel (System->Build_dir->USB)"
	@echo "	 	make cpscripts   -- Copy COMLIN scripts to USB drive "
	@echo 
	@echo "   For more information type 'make help3'"
	@echo 
	@echo " *Warning! Make sure config_build:RDDEV points to a jump drive!" 
	@echo "      !!!! Specifying the wrong drive will destroy data !!!! " 
	@echo 

help3:
	@echo 
	@echo "Making a bootable jump drive. *(see Warning! at end)"
	@echo 
	@echo "Shortcuts:"
	@echo 
	@echo "	 	make c            -- alias for make cycle"
	@echo "	 	make u            -- alias for make umount"
	@echo "	 	make n            -- alias for make new"
	@echo "	 	make b            -- alias for make bigcycle"
	@echo "	 	make a            -- alias for make doall"
	@echo 
	@echo "Preparation: (optional)"
	@echo 
	@echo "	 	make getmods    -- Copy modules from system into build dir"
	@echo "	 	make getmods2   -- Copy modules from system into USB build dir"
	@echo "	 	make getkern    -- Copy kernel from system into build dir"
	@echo "	 	make getkern2   -- Copy kernel from system into USB dir"
	@echo "	 	make clean      -- Remove tmp and work files"
	@echo 
	@echo "   For more information type 'make help4'"
	@echo 	
	@echo " *Warning! Make sure config_build:RDDEV points to a jump drive!" 
	@echo "      !!!! Specifying the wrong drive will destroy data !!!! " 
	@echo 

help4:
	@echo 
	@echo "Making a bootable jump drive. (see Warning! at end)"
	@echo 
	@echo "To execute the whole set of commands in a batch operation:"
	@echo 
	@echo "	 	su root -c 'make doall'"
	@echo  	
	@echo "The 'su' command will not timeout like the sudo for the long "
	@echo "copy process;"
	@echo 	
	@echo "The 'make doall2' target will not promp for confirmation. Mainly"
	@echo "useful for scripts"	
	@echo 	
	@echo "	 	make getimg     -- Get COMLIN drive image"
	@echo 	
	@echo " *Warning! Make sure config_build:RDDEV points to a jump drive!" 
	@echo "      !!!! Specifying the wrong drive will destroy data !!!! " 
	@echo 

prompt:
	@./scripts/prompt.sh " fdisk / format "
	@echo "Prompt succeeded ..."    

detect:	
	sudo ./scripts/make_detect

new: prompt	
	sudo ./scripts/make_part go
	sudo ./scripts/make_fs go
	@echo "Remove and Reinsert drive for next steps"

new2:
	sudo ./scripts/make_part go
	sudo ./scripts/make_fs go

initrd:
	@sudo ./scripts/make_initrd do

initfs:
	@sudo ./scripts/make_initramfs

getusb:
	@sudo ./scripts/make_getusb

getusblite:
	@sudo ./scripts/make_getusb_lite

getusb2:
	@sudo ./scripts/make_getusb -u

copy:
	@sudo scripts/make_usb

syslin:
	@sudo ./scripts/make_syslin go
	
cleanusb:
	@sudo ./scripts/make_cleanusb

copyusb:
	@sudo ./scripts/make_copyusb
	
cycle: putkern syslin cpscripts umount
	@echo "Done Cycle"

bigcycle: copyusb putkern syslin cpscripts umount
	@echo "Done BigCycle"

doall: prompt new remnt copyusb putkern syslin cpscripts uremnt
	@echo "Done doall"

# Callable from scripts, will not prompt
doall2: new2 remnt copyusb putkern syslin cpscripts uremnt
	@echo "Done doall"

# ------------------------------------------------------------------------

remnt:
	./scripts/make_remount

uremnt:
	./scripts/make_uremount

getkern:
	@echo Getting new kernel
	sudo ./scripts/make_getkern

getkern2:
	@echo Getting new kernel
	sudo ./scripts/make_getkern2

getmods:
	@echo Getting new modules
	sudo ./scripts/make_getmods

getmods2:
	@echo Getting new modules to USB build dir
	sudo ./scripts/make_getmods2

putmods:
	@echo Putting new modules
	@sudo ./scripts/make_putmods

putkern:
	@echo Putting new kernel
	@sudo ./scripts/make_putkern go

refresh:	getkern getmods putmods putkern

umount:
	@sudo ./scripts/make_umount
	@echo "Wait for USB drive inactivity. Then you may remove drive."

cpscripts:
	@sudo ./scripts/make_cpscripts
    
backup:
	@sudo ./backup.sh
    
pack:
	@sudo ./pack.sh

clean:
	@sudo ./clean.sh

getimg:
	@sudo ./scripts/make_getimg

# ------------------------------------------------------------------------
# Shortcuts for PG  letter -> dependency

n:	new

u:	umount

c:	cycle

b:	bigcycle

a:	doall

# End of Makefile







