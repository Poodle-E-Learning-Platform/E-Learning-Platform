-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema learning_platform
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema learning_platform
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `learning_platform` DEFAULT CHARACTER SET latin1 ;
USE `learning_platform` ;

-- -----------------------------------------------------
-- Table `learning_platform`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `learning_platform`.`users` (
  `user_id` INT(11) NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(45) NULL,
  `password` VARCHAR(45) NOT NULL,
  `is_admin` TINYINT NULL DEFAULT 0,
  PRIMARY KEY (`user_id`),
  UNIQUE INDEX `admin_id_UNIQUE` (`user_id` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `learning_platform`.`teachers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `learning_platform`.`teachers` (
  `teacher_id` INT(11) NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(255) NOT NULL,
  `first_name` VARCHAR(100) NOT NULL,
  `last_name` VARCHAR(100) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `phone_number` VARCHAR(20) NULL DEFAULT NULL,
  `linkedin_account` VARCHAR(255) NULL DEFAULT NULL,
  `users_user_id` INT NOT NULL,
  PRIMARY KEY (`teacher_id`),
  UNIQUE INDEX `email` (`email` ASC) VISIBLE,
  INDEX `fk_teachers_users1_idx` (`users_user_id` ASC) VISIBLE,
  CONSTRAINT `fk_teachers_users1`
    FOREIGN KEY (`users_user_id`)
    REFERENCES `learning_platform`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `learning_platform`.`courses`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `learning_platform`.`courses` (
  `course_id` INT(11) NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(255) NOT NULL,
  `description` TEXT NOT NULL,
  `objectives` TEXT NOT NULL,
  `owner_id` INT(11) NOT NULL,
  `is_premium` TINYINT(4) NULL DEFAULT 0,
  `rating` DECIMAL(3,2) NULL DEFAULT 0.00,
  PRIMARY KEY (`course_id`),
  UNIQUE INDEX `title` (`title` ASC) VISIBLE,
  INDEX `owner_id` (`owner_id` ASC) VISIBLE,
  CONSTRAINT `courses_ibfk_1`
    FOREIGN KEY (`owner_id`)
    REFERENCES `learning_platform`.`teachers` (`teacher_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `learning_platform`.`course_tags`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `learning_platform`.`course_tags` (
  `tag_id` INT(11) NOT NULL AUTO_INCREMENT,
  `tag_name` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`tag_id`),
  UNIQUE INDEX `tag_name` (`tag_name` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `learning_platform`.`course_tag_mapping`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `learning_platform`.`course_tag_mapping` (
  `course_id` INT(11) NOT NULL,
  `tag_id` INT(11) NOT NULL,
  PRIMARY KEY (`course_id`, `tag_id`),
  INDEX `tag_id` (`tag_id` ASC) VISIBLE,
  CONSTRAINT `course_tag_mapping_ibfk_1`
    FOREIGN KEY (`course_id`)
    REFERENCES `learning_platform`.`courses` (`course_id`),
  CONSTRAINT `course_tag_mapping_ibfk_2`
    FOREIGN KEY (`tag_id`)
    REFERENCES `learning_platform`.`course_tags` (`tag_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `learning_platform`.`sections`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `learning_platform`.`sections` (
  `section_id` INT(11) NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(255) NOT NULL,
  `content` VARCHAR(225) NOT NULL,
  `description` TEXT NULL DEFAULT NULL,
  `external_resource` VARCHAR(255) NULL DEFAULT NULL,
  `course_id` INT(11) NOT NULL,
  PRIMARY KEY (`section_id`),
  INDEX `course_id` (`course_id` ASC) VISIBLE,
  CONSTRAINT `sections_ibfk_1`
    FOREIGN KEY (`course_id`)
    REFERENCES `learning_platform`.`courses` (`course_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `learning_platform`.`students`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `learning_platform`.`students` (
  `student_id` INT(11) NOT NULL AUTO_INCREMENT,
  `users_user_id` INT(11) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `first_name` VARCHAR(100) NOT NULL,
  `last_name` VARCHAR(100) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`student_id`),
  UNIQUE INDEX `student_id_UNIQUE` (`student_id` ASC) VISIBLE,
  INDEX `fk_students_users1_idx` (`users_user_id` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE,
  CONSTRAINT `fk_students_users1`
    FOREIGN KEY (`users_user_id`)
    REFERENCES `learning_platform`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `learning_platform`.`enrollments`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `learning_platform`.`enrollments` (
  `students_student_id` INT(11) NOT NULL,
  `courses_course_id` INT(11) NOT NULL,
  PRIMARY KEY (`students_student_id`, `courses_course_id`),
  INDEX `fk_students_has_courses_courses1_idx` (`courses_course_id` ASC) VISIBLE,
  INDEX `fk_students_has_courses_students1_idx` (`students_student_id` ASC) VISIBLE,
  CONSTRAINT `fk_students_has_courses_students1`
    FOREIGN KEY (`students_student_id`)
    REFERENCES `learning_platform`.`students` (`student_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_students_has_courses_courses1`
    FOREIGN KEY (`courses_course_id`)
    REFERENCES `learning_platform`.`courses` (`course_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `learning_platform`.`students_has_sections`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `learning_platform`.`students_has_sections` (
  `students_student_id` INT(11) NOT NULL,
  `sections_section_id` INT(11) NOT NULL,
  PRIMARY KEY (`students_student_id`, `sections_section_id`),
  INDEX `fk_students_has_sections_sections1_idx` (`sections_section_id` ASC) VISIBLE,
  INDEX `fk_students_has_sections_students1_idx` (`students_student_id` ASC) VISIBLE,
  CONSTRAINT `fk_students_has_sections_students1`
    FOREIGN KEY (`students_student_id`)
    REFERENCES `learning_platform`.`students` (`student_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_students_has_sections_sections1`
    FOREIGN KEY (`sections_section_id`)
    REFERENCES `learning_platform`.`sections` (`section_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
