export class Course {
  courseSec: string;
  courseTitle: string;
  classType: string;
  creditHours: string;
  gradeType: string;
  classDays: string;
  startTime: string;
  endTime: string;
  instructor: string;
  maxSeats: string;
  currentSeats: string;
  remainingSeats: string;
  constructor(
    courseSec: string,
    courseTitle: string,
    classType: string,
    creditHours: string,
    gradeType: string,
    classDays: string,
    startTime: string,
    endTime: string,
    instructor: string,
    maxSeats: string,
    currentSeats: string,
    remainingSeats: string
  ) {
    this.courseSec = courseSec;
    this.courseTitle = courseTitle;
    this.classType = classType;
    this.creditHours = creditHours;
    this.gradeType = gradeType;
    this.classDays = classDays;
    this.startTime = startTime;
    this.endTime = endTime;
    this.instructor = instructor;
    this.maxSeats = maxSeats;
    this.currentSeats = currentSeats;
    this.remainingSeats = remainingSeats;
  }

  print() {
    console.log(
      "[" + this.courseSec,
      this.courseTitle,
      this.classType,
      this.creditHours,
      this.gradeType,
      this.classDays,
      this.startTime,
      this.endTime,
      this.instructor,
      this.maxSeats,
      this.currentSeats,
      this.remainingSeats + "]"
    );
  }
}
