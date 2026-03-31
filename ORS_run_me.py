import ashes_fg as af
from ashes_fg.examples import ors_buffer, cs_amp, my_design

af.fpaa.compile(my_design, project_name='my_design', chip_num=16)