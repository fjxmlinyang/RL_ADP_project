- SystemSetUp

  - PshSystem
    - set_up_parameter

  - ESystem
    - set_up_parameter

  - LMP
    - set_up_parameter

- OptModelSetUp

  - ___init__
    - initial self.model 这里直接就把initial 放进去然后计算

  - add_var_e

  - add_var_I

  - add_var_psh

  - set_up_main

    - set_up_constraint #add

      - add_constraint_rolling

      - add_constraint_epsh

      - add_constraint_curve

      - add_constraint_soc

      - add_constraint_I

      - add_constraint_terminal

    - set_up_variable

    - set_up_object

  - solve_model_main

    - gur_model.setObjective

    - gur_model.optimize

  - get_optimal_main #get

    - get_optimal_soc

    - get_optimal_gen_pump

    - get_optimal_profit应该是在这里改

    - get_curr_cost

    - output_optimal

  - optimization_model_with_input

    - 应该在这里加第一个

    - set_up_main

    - solve_model_main

    - 在这里加第二个

    - get_optimal_main #get 

  - x_to_soc

- Multiprocess_Cal这里直接就把initial 放进去然后计算

  - calculate_new_soc

- Curve

  - seg_initial

  - seg_update

  - curve_initial

  - show_curve

  - curve_update

  - input_curve

  - output_initial_curve

- CurrModelPara

  - self.LAC_last_windows = LAC_last_windows

  - self.RT_DA = RT_DA

  - self.probabilistic = probabilistic

  - self.date = date

  - self.LAC_bhour = LAC_bhour

  - self.scenario = scenario

  - self.current_stage = current_stage

- Kernel

  - ___init__

  - main_function

    - calculate_optimal_soc    # main optimization soc

    - calculate_new_soc     # optimization project for any input

    - get_final_curve_main    # main function for update curve

      - get_new_curve_step_1    找到新的curve

        - self.curve

        - self.second_curve_profit新的curve的profit创建

        - self.second_curve_slope新的curve的slope创建

      - get_new_curve_step_2_curve_comb 组合起来
        - α\alphaα *self.old_curve + (1−α)(1-\alpha)(1−α)self.second_curve

      - get_new_curve_step_3_two_pts 找到convex的两个点

        - self.second_point_soc_sum/self.second_point_profit

        - self.previous_point_soc_sum/self.previous_point_profit 

        - self.pre_scen_optimal_profit

        - 

      - curve.curve_update 保证convex的update

      - output_curve 输出

      - output_curve_sum 输出