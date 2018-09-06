{% extends "header.vhd" %}
{% block code %}
-- Description:
-- Package for constants depending on L1Menu.

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;
use ieee.numeric_std.all;

use work.lhc_data_pkg.all;
use work.math_pkg.all;
use work.gt_mp7_core_pkg.all;

package constants_pkg is
-- Module ID
constant MODULE_ID : integer := {{ module.id|int }};

-- Menu ID (128 bits = 4 x 32 bits)
constant L1TM_UID : std_logic_vector(127 downto 0) := X"{{ module.menu.uuid|hexuuid }}";

-- Menu name (1024 bits = 32 x 32 bits, 128 ASCII-characters, right to left)
constant L1TM_NAME : std_logic_vector(128*8-1 downto 0) := X"{{ module.menu.name|hexstr(128) }}";

-- Distribution ID, provided to keep track of multiple menu implementations.
constant L1TM_FW_UID : std_logic_vector(127 downto 0) := X"{{ module.menu.dist_uuid|hexuuid }}";

-- Code generator version
constant L1TM_SW_VERSION_MAJOR : integer range 0 to 255 := {{ meta.proc.version.version[0]|int }};
constant L1TM_SW_VERSION_MINOR : integer range 0 to 255 := {{ meta.proc.version.version[1]|int }};
constant L1TM_SW_VERSION_REV   : integer range 0 to 255 := {{ meta.proc.version.version[2]|int }};
constant L1TM_COMPILER_VERSION : std_logic_vector(31 downto 0) := X"00" &
    std_logic_vector(to_unsigned(L1TM_SW_VERSION_MAJOR, 8)) &
    std_logic_vector(to_unsigned(L1TM_SW_VERSION_MINOR, 8)) &
    std_logic_vector(to_unsigned(L1TM_SW_VERSION_REV, 8));

-- Tracking git/svn revision (to be reorganized)
constant SVN_REVISION_NUMBER : std_logic_vector(31 downto 0) := X"00000000";

-- Hash sum of menu ID
constant L1TM_UID_HASH : std_logic_vector(31 downto 0) := X"{{ module.menu.name|mmhashn|hex(8) }}";

-- Hash sum of firmware ID
constant FW_UID_HASH : std_logic_vector(31 downto 0) := X"{{ module.menu.dist_uuid|mmhashn|hex(8) }}";

-- Configure used algorithms
type used_algos_array is array (0 to MAX_NR_ALGOS-1 ) of boolean;
constant USED_ALGOS : used_algos_array := (
{%- for seed in seeds %}
    {{ seed.index }} => true,
{%- endfor %}
    others => false
);

end package;
{% endblock code %}
